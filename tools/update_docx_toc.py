#!/usr/bin/env python3
"""Fill in the Word table of contents (page numbers) using LibreOffice headless.
Usage: python3 tools/update_docx_toc.py book/Practical-Game-Theory.docx"""
import os, subprocess, sys, tempfile, textwrap
path = os.path.abspath(sys.argv[1])
macro = textwrap.dedent(f"""
import uno
from com.sun.star.beans import PropertyValue
def pv(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p
ctx = uno.getComponentContext()
desk = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
url = uno.systemPathToFileUrl({path!r})
doc = desk.loadComponentFromURL(url, "_blank", 0, (pv("Hidden", True),))
idx = doc.getDocumentIndexes()
for i in range(idx.getCount()):
    idx.getByIndex(i).update()
doc.refresh()
doc.storeToURL(url, (pv("FilterName", "MS Word 2007 XML"),))
doc.close(True)
""")
with tempfile.TemporaryDirectory() as td:
    script = os.path.join(td, "upd.py")
    open(script, "w").write(macro)
    soffice = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore",
        f"-env:UserInstallation=file://{td}/profile",
        "--accept=socket,host=127.0.0.1,port=2083;urp;"])
    try:
        runner = textwrap.dedent(f"""
        import time, uno
        local = uno.getComponentContext()
        res = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        for _ in range(60):
            try:
                ctx = res.resolve("uno:socket,host=127.0.0.1,port=2083;urp;StarOffice.ComponentContext"); break
            except Exception: time.sleep(1)
        src = open({script!r}).read().replace("ctx = uno.getComponentContext()", "")
        exec(src, {{"uno": uno, "ctx": ctx}})
        """)
        subprocess.run(["python3", "-c", runner], check=True)
    finally:
        soffice.terminate()
print("updated TOC in", path)
