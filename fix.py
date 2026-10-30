from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
d=Document('raw.docx')
for s in d.sections:
    s.left_margin=s.right_margin=Cm(2.3); s.top_margin=s.bottom_margin=Cm(2.2)
usable=21.0-4.6
def setfont(st,name,size=None):
    st.font.name=name
    rpr=st.element.get_or_add_rPr(); rf=rpr.find(qn('w:rFonts'))
    if rf is None: rf=OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(a),name)
    if size: st.font.size=Pt(size)
for st in d.styles:
    try:
        if st.type!=1: continue
    except: continue
    n=st.name
    if n.lower().startswith('heading'): setfont(st,'Liberation Sans'); st.font.color.rgb=RGBColor(0x1F,0x3F,0x7A)
    elif n in('Verbatim Char','Source Code'): setfont(st,'Liberation Mono',8.5)
    elif n in('Body Text','First Paragraph','Compact','Image Caption','Table Caption'): setfont(st,'Liberation Serif',11 if 'Body' in n or 'First' in n else 10)
    elif n in('Title','Subtitle','Author','Date'): setfont(st,'Liberation Sans')
for st in d.styles:
    if st.name.lower()=='heading 1': st.font.size=Pt(16)
    if st.name.lower()=='heading 2': st.font.size=Pt(13)
def borders(tbl):
    pr=tbl._tbl.tblPr
    b=OxmlElement('w:tblBorders')
    for e in('top','left','bottom','right','insideH','insideV'):
        x=OxmlElement('w:'+e); x.set(qn('w:val'),'single'); x.set(qn('w:sz'),'4'); x.set(qn('w:color'),'888888'); b.append(x)
    pr.append(b)
for t in d.tables:
    borders(t)
    for i,r in enumerate(t.rows):
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.size=Pt(9.5)
                    if i==0: run.bold=True
            if i==0:
                tcPr=c._tc.get_or_add_tcPr(); sh=OxmlElement('w:shd')
                sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),'DCE6F5'); tcPr.append(sh)
# images: fit width
for sh in d.inline_shapes:
    w,h=sh.width,sh.height
    maxw=Cm(usable); maxh=Cm(19.5) if h>w*1.5 else Cm(15.5)
    k=min(maxw/w,maxh/h,1.0) if True else 1
    k=min(maxw/w,maxh/h)
    sh.width=int(w*k); sh.height=int(h*k)

from docx.shared import Cm as C
for t in d.tables:
    t.autofit=False
    n=len(t.columns); h0=t.rows[0].cells[0].text.strip()
    if h0=='ID': ws=[1.8]+[None]*(n-1)
    else: ws=[3.6]+[None]*(n-1)
    if h0=='ID' and n==4 and 'Kategori' in t.rows[0].cells[1].text: ws=[1.9,2.3,None,3.2]
    if h0=='ID' and n==4 and 'Prioritas' in t.rows[0].cells[2].text: ws=[1.6,None,1.7,2.0]
    if h0=='ID' and n==5: ws=[1.8,3.2,3.4,None,2.8]
    rest=usable-sum(w for w in ws if w); k=sum(1 for w in ws if w is None)
    ws=[w if w else rest/k for w in ws]
    for r in t.rows:
        for c,w in zip(r.cells,ws): c.width=C(w)
    grid=t._tbl.tblGrid
    for gc,w in zip(grid.findall(qn('w:gridCol')),ws): gc.set(qn('w:w'),str(int(w*567)))
    tw=t._tbl.tblPr.find(qn('w:tblW'))
    if tw is None: tw=OxmlElement('w:tblW'); t._tbl.tblPr.append(tw)
    tw.set(qn('w:type'),'dxa'); tw.set(qn('w:w'),str(int(usable*567)))
    lay=OxmlElement('w:tblLayout'); lay.set(qn('w:type'),'fixed'); t._tbl.tblPr.append(lay)
for p in d.paragraphs:
    if p.text.strip().startswith('Flowchart Proses') or p.text.strip().endswith('Flowchart Proses Barang Keluar'):
        p.paragraph_format.page_break_before=True
d.save('Dokumentasi-SIIB.docx')
