
# <span style="color:blue; font-size:16;">Eample saspy notebook showing the python interface to SAS</span>

# Import HTML to use to display results from the LST


```python
from IPython.display import HTML 
```

# Import the saspy module to get access to SAS 


```python
import saspy
```

### Instantiate a SASsession object. This creates the SAS session that will be used for this notebook


```python
sas = saspy.SASsession()
```

    Please enter the name of the SAS Config you wish to run. Available Configs are: ['default', 'http', 'httptest', 'ssh'] default
    SAS Connection established. Subprocess id is 8255


### Delete the '#' sign bellow (comment), and put the cursor after the dot (.) and hit Tab. It will show you the methods available from the SASsession object


```python
#sas.
```

### Create a SASdata object to use to access the cars data set in the sashelp library. 


```python
cars = sas.sasdata('cars', libref='sashelp')
```

### Again, remove the comment character, #, and after the dot, hit Tab to see the methods available on the SASdata object


```python
#cars.
```


```python
#cars.describe()
#cars.head()
cars.tail()
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="Print" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">The SAS System</span> </p>
</div>
<h1 class="contentprocname toc">The PRINT Procedure</h1>
<article>
<h1 class="contentitem toc">Data Set SASHELP.CARS</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/></colgroup><colgroup><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/></colgroup>
<thead>
<tr>
<th class="r header" scope="col">Obs</th>
<th class="header" scope="col">Make</th>
<th class="header" scope="col">Model</th>
<th class="header" scope="col">Type</th>
<th class="header" scope="col">Origin</th>
<th class="header" scope="col">DriveTrain</th>
<th class="r header" scope="col">MSRP</th>
<th class="r header" scope="col">Invoice</th>
<th class="r header" scope="col">EngineSize</th>
<th class="r header" scope="col">Cylinders</th>
<th class="r header" scope="col">Horsepower</th>
<th class="r header" scope="col">MPG_City</th>
<th class="r header" scope="col">MPG_Highway</th>
<th class="r header" scope="col">Weight</th>
<th class="r header" scope="col">Wheelbase</th>
<th class="r header" scope="col">Length</th>
</tr>
</thead>
<tbody>
<tr>
<th class="r rowheader" scope="row">424</th>
<td class="data">Volvo</td>
<td class="data">C70 LPT convertible 2dr</td>
<td class="data">Sedan</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="r data">$40,565</td>
<td class="r data">$38,203</td>
<td class="r data">2.4</td>
<td class="r data">5</td>
<td class="r data">197</td>
<td class="r data">21</td>
<td class="r data">28</td>
<td class="r data">3450</td>
<td class="r data">105</td>
<td class="r data">186</td>
</tr>
<tr>
<th class="r rowheader" scope="row">425</th>
<td class="data">Volvo</td>
<td class="data">C70 HPT convertible 2dr</td>
<td class="data">Sedan</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="r data">$42,565</td>
<td class="r data">$40,083</td>
<td class="r data">2.3</td>
<td class="r data">5</td>
<td class="r data">242</td>
<td class="r data">20</td>
<td class="r data">26</td>
<td class="r data">3450</td>
<td class="r data">105</td>
<td class="r data">186</td>
</tr>
<tr>
<th class="r rowheader" scope="row">426</th>
<td class="data">Volvo</td>
<td class="data">S80 T6 4dr</td>
<td class="data">Sedan</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="r data">$45,210</td>
<td class="r data">$42,573</td>
<td class="r data">2.9</td>
<td class="r data">6</td>
<td class="r data">268</td>
<td class="r data">19</td>
<td class="r data">26</td>
<td class="r data">3653</td>
<td class="r data">110</td>
<td class="r data">190</td>
</tr>
<tr>
<th class="r rowheader" scope="row">427</th>
<td class="data">Volvo</td>
<td class="data">V40</td>
<td class="data">Wagon</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="r data">$26,135</td>
<td class="r data">$24,641</td>
<td class="r data">1.9</td>
<td class="r data">4</td>
<td class="r data">170</td>
<td class="r data">22</td>
<td class="r data">29</td>
<td class="r data">2822</td>
<td class="r data">101</td>
<td class="r data">180</td>
</tr>
<tr>
<th class="r rowheader" scope="row">428</th>
<td class="data">Volvo</td>
<td class="data">XC70</td>
<td class="data">Wagon</td>
<td class="data">Europe</td>
<td class="data">All</td>
<td class="r data">$35,145</td>
<td class="r data">$33,112</td>
<td class="r data">2.5</td>
<td class="r data">5</td>
<td class="r data">208</td>
<td class="r data">20</td>
<td class="r data">27</td>
<td class="r data">3823</td>
<td class="r data">109</td>
<td class="r data">186</td>
</tr>
</tbody>
</table>
</article>
</section>
</body>
</html>




```python
for col in ['horsepower','MPG_City', 'MSRP']:
    cars.hist(col, title='Histogram showing '+col.upper())
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="SGPlot" data-sec-type="proc">
<h1 class="contentprocname toc">The SGPLOT Procedure</h1>
<article id="IDX">
<h1 class="contentitem toc">The SGPlot Procedure</h1>
<div class="c">
<img style="height: 480px; width: 640px" alt="The SGPlot Procedure" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAIAAAC6s0uzAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAgAElEQVR4nOzdeVxU970//vc5sw/DJoiACAjIDqKAIi5RY9aaZmsTb9LEaL1Nqqk3aX5p782N+r35tWn7yDdN++0t+aWXqk3SxJ/GpCaGqkkMUURFWWUXEBDZdwaGYWbO+f5xEjIBZBP4zPJ6PvLIYzycmfOaA8yLs30OV1hYSAAAADC35EQUHx/POgYAAIATKSoq4llnAAAAcEYoYAAAAAZQwAAAAAyggAEAABhAAQMAADCAAgYAAGAABQwAAMAAChgAAIABFDAAAAADKGAAAAAGUMAAAAAMoIABAAAYQAGDfeA4juO4cSauXr169erVc55rLoz53m/dzK6xCb9Bkr/+9a+rVq3SarVarXbVqlUHDhwYPf8wrVa7du3aI0eOWM/z4Ycfrl27VqvVKpXKpKSk3//+92azecynDxv9VaVSGRkZ+be//W1E4HHi+fn5cRzX1NRERIIgyOVyjuPkcrkgCETU1tbGcdz8+fOnFONm7xGcRWFhoQhg86Qf13EmpqampqamTuNFbN8sxZ7MGpu8Cb9Boiju2LFj9EfQT3/60xHzj/bmm29KM7z77rujv7p+/frxnz7OV48dOzbJeA8//PDw/BcuXBieISsrSxTFTz75hIgefPDB6cWwfo/gJAoLC7EFDA7i3Llz586dY53CnszxGsvIyEhPT9doNAcPHjSZTCaT6eDBgxqN5s033zxx4oT1nMOfUP39/S+//DIR/e53v5O+tHfvXiI6dOiQxWKxWCyZmZn333//v/3bv4359GGjv2qxWF599VUiev311ycZb+nSpURUWVlJRFVVVUTk6elJRDU1NcNTwsPDpxRjzPcITgRbwGAXpB/XcSZaP66urt60aZNGo1GpVBs3bjx58qQ4astDmnP//v1LlixRKBRLlizZv3+/9YsfOnQoIiLCx8fnjTfeGL2gkpKSwMDAkJAQURSzsrIefvhhV1dXlUp11113NTY2Ws/53nvvRUREuLu7v/322y+++KKLi4uvr+9nn302+j2OGXv4ddLT00NCQhQKxYoVK6qrq4efNfottLe3E5GLi4vFYhFF8fDhw0R09OhRURQtFouLi4tMJpPmGfGmbraIm62KKX2D7r//fiL64x//aD3DH//4RyK67777xn8RhUIhPXZxcSGiTz/9dHSAmz19nK9av/KE8T766CMieuyxx0RR/MlPfiI9JqLt27eLoig9llbyVGOMSAJOorCwEAUM9mGcPyKtZ5AeR0VFWc8g1eToZ0nNZE36AB3zSyMWtGbNGiJ68sknRVFcsmSJ9Wz33HPPhJmXLl06+j2OGXvM11mzZs3NckpvYd26dUQk1fyuXbuI6N/+7d9EUfzss8+Gnz76TU1yETTR5t2YM7u6uhJRZ2en9bN6enqIyNXVdfQ3URRFk8n0q1/9ioji4uKkKb/85S+lefz9/bdv3/7pp59Kf2SMk2HEV6XHw1vAwyt5wnjSnyzSN27Tpk1E9Omnn9I3O8ATExOJ6OrVq1OKMeZ7BCeBAga7MeHnu/VjlUpFRG+99ZbBYDh8+PALL7wweh5RFFNSUojot7/9rSiKr7zyChGtWLHC+kt79+4VRfFPf/rT6AXFxMQ0NzdLU1588cX9+/ebTKaKigoiUqlU1nO+9dZbDQ0Nw49ra2vpJps748d+8skn+/v7T58+bf30m72F1157jb4pXWke6XCvtLdWmn/0m/rZz35mNBrHXMSYq2JK3yCFQnGzJw4v62avYH2k9tVXX42IiBj+UkhISEVFxThPHz/h8CbvZOJ5enoqFAqLxaJSqTQajfQtU6lUFotFoVCM+L5PKcaI9wjOAAUMdmPEp9joidaPpT2HROTv7//uu+/e7EWkz1xpE8pkMhGR9Kk6/CWTyXSzBZ05c2b4dQwGw8svvxwXF6fRaG4W6WaPrU0ytvU/b/YWysrKiCgkJMRkMslksoCAAJlMZjKZgoODiaikpGT8SKMXMeaquNn3YsyJk98Ctubv75+TkzN6cWVlZW+88UZcXBx987fFONlGv7hMJouJibE+72ky8R588EH6ZsN348aN4jd7GqQzsEacCzaZGOO/R3BsKGCwGxN+vo+Y4cqVK0899ZRMJiOiX/7yl2POM04BS08c3r05zoLEb86PtTb+s8b5gJ5MbOt/jvMWpB3jUqlLW67SEdwRe7YnXMQ4q8LahN8gaS2NeZD14YcfHj1/dna2VIqHDh0ac12JomgwGGjULoebzTz+VycTTzoFTDrc+5Of/EQUxaeeeoqItmzZQt8cDJ5SjMm8R3BUKGCwG1Mq4Jdeekk6gyk7O9u6k6R5hk+Sknau/upXvxK/+WxNSUmRviSd8ip9aXjD9GZJpBbMz89/8803b6WAx4895rse5y08//zzRBQcHOzp6SmKoo+Pj7T5K+2XHj+S9T/HWRU3+16MOfHMmTPSm9q/f790DvP+/fulfQaZmZljvkhmZqZGo9FoNJcvX5amHDt27K677vrnP/9pMpksFouUJzg4ePwVO5mvTiaedB6Wt7c3Eb333nuiKL799tvDU4Z3Wkwpxuj3CE4CBQx2Y0oFPOKsqIiICGn68FlO0slT45yEJX2wjnCzJIGBgRPOOf4rjB97xPzW/xznLWRmZkpTtmzZIoqitJVG35yZNX4k63+Osyqm9A0SRVG63maEl19+eZwXOXnypEKh8Pf3l464b9y4cfQrDJ++PvpL47zH0SaM19jYODxd2mmclZU1PEW6IHgaMUa8R3ASKGCwGxN+vls//uSTT9atWyeTyaTrea5cuSJNz87OjomJkclkw7thDx48KNXe6MuQ3n777ZCQEHd3d2nPrUwmu1mSo0ePuru7+/j4vPnmm76+vvTNRvbN4t2sCW4We8T8I/55s7dgsVjc3d3pm221Q4cOkdW1SeNHGvHPm60KaxN+g4bX1bp166Rzl9atW3f48OEJX+TYsWMymWzFihUGg8Fisfz5z3+WXkGhUKxZs+aTTz4Z8fTJN99o48cTvzlULJ2KJYqidIhdWicjVuyUYli/x/ETgsMoLCzkCgsL4+Pjb/YTA+CcfvGLX0RERDzxxBM8z//ud797+eWXg4ODr127xjoXA1gVALOhqKhIzjoDgC06evRoTU2N9diE0iFVJ4RVATBLZD/96U8XLFjAOgaAbYmIiGhpaWlqapLJZAkJCb/+9a+feeYZ1qHYwKoAmA0tLS3YBQ0AADDXioqKcDMGAAAABlDAAAAADKCAAQAAGEABAwAAMIACBgAAYAAFDAAAwAAKGAAAgAHGI2GZzebXXnvtpZdeEr8ZIjUjI+P1118/f/48ET388MO///3v58+fT0RpaWmvv/46Eb3wwgs7d+6c8JX/fuRDvV4/m9kBAADG5u+74L577hp/HsYFrNPpNm3aZD3lnXfeeeaZZ06ePMnz/Pvvv//EE0+cOHHiwIEDR44cycnJUSgUjz32mEaj2bZt2/ivrNfrn9725GxmBwAAGNtbB8a4jdgIjAt4cHCQiDiOG57y/vvvDz9+/PHHpaJNT0//7W9/6+XlRUT79u177rnnJixgAAAAW2bTx4CLi4ulYTLz8/NXr14tTUxMTMzPz2eaCwAA4FbZ7t2QBgYGnn76aen+owaDgee//luB5/mhoSHrOYdMpst5BdZTFErFnOUEAACYBhst4I6OjkceeeTFF19cu3YtEWk0GkEQpA4WBEGpVFrPzHOcq6vOeopCbqPvCwAAQGKLRVVaWvrjH//4D3/4w8qVK6UpycnJZ8+eve2224goNzd32bJl1vPL5fK46KgRL/LVufNzkxYAAGAabO4Y8IkTJ3bt2vXhhx8Oty8Rbd++fe/evW1tbV1dXXv27LG+NzgAAIA9srkt4HvuuYeI/P39h6eIorh169b+/v6UlBQiev7553EKNAAA2DubKODhUThGPLa2c+fOyYy/AQAAYBdsbhc0AACAM0ABAwAAMIACBgAAYAAFDAAAwAAKGAAAgAEUMAAAAAMoYAAAAAZQwAAAAAzYxEAcAI5HFEVBEBgG4Hne+k7bAGBrUMAAs+Lo0aOPPPLI8G0055ggCLt2//z//OF/o4EBbBYKGGC23HHX5l+9/v8xWfTB//mTvr+fRJGwEQxgq3AMGAAAgAEUMAAAAAMoYAAAAAZQwAAAAAyggAEAABhAAQMAADCAAgYAAGAABQwAAMAAChgAAIABFDAAAAADKGAAAAAGUMAAAAAMoIABAAAYQAEDAAAwgAIGAABgAAUMAADAAAoYAACAARQwAAAAAyhgAAAABlDAAAAADKCAAQAAGEABAwAAMIACBgAAYAAFDAAAwAAKGAAAgAEUMAAAAAMoYAAAAAZQwAAAAAyggAEAABhAAQMAADCAAgYAAGAABQwAAMAAChgAAIABFDAAAAADKGAAAAAGUMAAAAAMoIABAAAYQAEDAAAwwLiAzWbzb37zG47jrCempaWFhoaGhoampaWNPxEAAMBOydkuXqfTbdq0yXrKgQMHjhw5kpOTo1AoHnvsMY1Gs23btjEnssoMAABw6xhvAQ8ODh4/ftx6Snp6+iuvvOLl5eXm5rZv37709PSbTQQAALBfjLeAR8vPz1+9erX0ODExMT8//2YTh5ktlmu1ddZT5HKbe18AAADWbK6oDAYDz3+9Xc7z/NDQ0M0mDhMslus3Gq2nqJTKOQkLAAAwTTZXwBqNRhAEqW4FQVAqlTebOEypVG5ct2bE6xSXlc9VZAAAgCmzucuQkpOTz549Kz3Ozc1dtmzZzSYCAADYL5sr4O3bt+/du7etra2rq2vPnj07duy42UQAAAD7ZXO7oLdu3drf35+SkkJEzz//vHS50ZgTAQAA7JdNFLAoitb/3Llz586dO0fMM+ZEAAAAO2Vzu6ABAACcAQoYAACAARQwAAAAAyhgAAAABlDAAAAADKCAAQAAGEABAwAAMGAT1wEDOC2LRejq1Q8aTQODQ4ZBoyiQVquS8byHm3aeu47jONYBAWC2oIABGOjo7quua+7s6W/r6DGazGPOw3Hc/HmuwQELFi7w9PJwneOEADDbUMAAc8doMl+91ni1trmju0+aIpPxnu46F41Kq1Zq1CoiMgwae/WGvn5Dv8HY2tHb2tFLRIF+3vFRQb7eHizTA8CMQgEDzAWT2ZJfUlNR0yht77poVIsXLQhaON/b01Uhl435FMOgsaah7UZTR31Tu/Sfj5dbZGhAeLDf3GYHgFmBAgaYdfVN7ecul/cbjETk6+0RHxW00GeeTDbBKZAatSomLCAmLMBoMlfUNJZWNbR29LZ2lNbUtyTHh2KnNIC9QwEDzCLDoPGrnLKG5g4ictdpblsZ6+PlNtUXUSnk8RGBceGLrtY1X8yvbGjuuNHSmRgTkhAdPPOJAWCuoIABZovG0+/DU5cMg0aZjE+MDY0LX3QrZzVzHBce7LfId97Fwurq+ubLxdU3Wjo2roqVjhwDgN3BdcAAs+Jqs8lnSaph0Ojt6fbQXSnxEYEzck2RRq1avzL6exuWu2hUTW3dhzPOS5vXAGB3UMAAM8xktqR/cLa23cxxfEJ08P2bktx1mpldhK+3xw/uWeXj5WYyWz47V1RefWNmXx8A5gAKGGAm9eoNr+0/eam4ViHjmkpOJ8WGztJgGgq57Pu3J0eGLrRYhKzc8pzCq7OxFACYPShggBnT1Tvw2/QTdY0d/j4eSYuVRv2s7xxekxi5NimK47iiivoLBehgAHuCAgaYGR3d+tf2n+zo1i/ynffCU3fq1HP0yxUR4n/HmniZjC+urD97uUwUxblZLgDcIhQwwAxobu8Zbt/nntyk087pmcmBft733LZMpZBX1DSevYQOBrAPKGCAW9WrN/z5vS+7egfCAn3mvn0lvt4e925YrlYpKmubsnLL5z4AAEwVChjglpjMljcPZbZ29gX5e+16bAOT9pV4ebjevS5BJuMrahoF1XxWMQBgklDAANMnCOKbhzJrGtp9vd13/+h2rVrJNo+3p9uda5ZyHCeo58t0C9iGAYDxoYABpu/Y6YKSqkYvD93uH21kuO1rbeGCeauXRxCRzG1RTUM76zgAcFMoYIBpulhUcyq7hOe5n265zctDxzrOtyJDF/JDXUTcf//9dGNrN+s4ADA2jAUNDqu7u/vEiROz9OI9BrGg3iyIFO0vO5d5avQMFy9eNFvMs7T0CfGGJrMoGyC3//ng7L/vuEelxG86gM3BryU4rLq6uqeffiZ13YYZf2WZQuUbuVGm1PQ0lZ/ILR1znorSYv+AoBlf9ORZumrmR65pbO3++/GL2x9azTAJAIwJBQyOzD9g0Su/+/OMv+yJMwUNzR2LA3w2/nDjzUaa/ONrr9TWVM34oidPFEw/e3zDr9/KuFhU4+/jfveaWIZhAGA0HAMGmJrLxdUNzR0uGtXqxMhZGud5pvh6uz+2eSURHTtdUFXfyjoOAHwHChhgCuqb2gvL6jiOW5scpVYpWMeZWGpC6O0pUYIgvnX4TK/ewDoOAHwLBQwwWYZB45mcUlEUl0UHB/h6sY4zWT+4MzEs0KdXb/jo83zWWQDgWyhggMn6Kqds0Gjy8XJbFr2YdZYp4Hlu+0OrVUp5dkH1lzkVrOMAwNdQwACTUlxZ39DcIZPx0u3/WMeZGi8P3eObVxLRR5/ntXb2sY4DAEQoYIDJ6NEbLl2pJqK1SZGe7jY05sbkrYwPSU0INQ6ZD3yYJQi4XRIAeyhggIllXSq1WITFAT6hgb6ss0zflntX+Hq71zS0XyiqYZ0FAFDAABMpr77R1NatUavWJNvfzmdrKqX8kbuTiOhQRk5Ht551HABnhwIGGE+/wXipqIqI1iZHqhR2P3BNTJi/tCMaZ0QDMIcCBhjP2UtlRpM5IsQ/0M+bdZaZ8cO7k9x0mkvFtZeKa1lnAXBqKGCAmyqvvtHQ3KFRq5JiQ1hnmTFatfKpB1KJ6PCJywODQ6zjADgvFDDA2AaNJmnnc0rCEo3aJu71O1NiwvzjwwN69YbjmUWsswA4LxQwwNguF1cbTWYfL7eQRT6ss8y8xzav1GlVX+aU1zS0s84C4KRQwABjuNbQWlHTyHHcuhXRdn3m8814umkfvjNREMR3Pj6Py4IBmEABA4xkMlsuFlaJohizZJGHqwvrOLMlNSE0JMC7sbX7VHYJ6ywAzggFDDBSadV1fb9B56JZFmNPYz5Pw8N3JhLRZ9ml+gEj6ywATgcFDPAd+n5DUVkdEa1cGuYAF/6OLyzQZ2V8iH7A+PfjF1lnAXA6KGCA77h0pdpoMvvN9wheOJ91lrlw/8alKqU8r7QOZ2MBzDEUMMC3Wjt6a663chy3Jtkxz70azctDt2FFJBG9h41ggLmFAgb41rncclEU4yOC3HUa1lnmzr3r4jzdtNebOy/iJg0Ac8jmCripqemhhx7SarVqtfqhhx5qaWmRpqelpYWGhoaGhqalpbFNCI7qWkNrR3efi0YVHxXEOsucUinlm9cvJaJjpwuNQ2bWcQCchc0V8JYtW5YtW9bb26vX6+Pi4rZs2UJEBw4cOHLkSE5OTn5+fkZGxoEDB1jHBEcjXXpERPFRwQ5/7tVoqQmh/j4eHd3645mFrLMAOAubK+Dz58/v2bNHLpfL5fJ9+/adO3eOiNLT01955RUvLy83N7d9+/alp6ezjgmOprC8Vt9v8PJwjVzszzoLAzzPPfVAKs9zX+ZU9OoNrOMAOAWbK+DNmzf/5S9/EQRhaGhoz5499957LxHl5+evXr1amiExMTE//zt3UhNFsbun1/q/3r4+BtHBbvUbjCWV14koZVm4TGZzvxRzI8jfKz48wGS2fHAqj3UWAKdgc7va/vrXv65aterpp58moiVLlkhbwAaDgee//ljkeX5o6Du3cBk0Gk9+cdp6ilqtnqu84AguFVWbzJaghfP95nuwzsLSI3cnFVU2XCyquXtNjL+PU68KgDlgc3/sb9u27dlnnzWZTBaL5bnnnvvxj39MRBqNRhAEaQZBEJRKpfVTNGr1ow89YP3f/ffezSA62Kfuvv7q+maO41YlLGGdhTEvD91tSeFE9MGpXNZZAByfzRVwRkbGs88+K5fLeZ7fuXPniRMniCg5Ofns2bPSDLm5ucuWLWOaERxK7pUaURTDF/vpXJzo0qOb2bx+qUopL6lqLKpsYJ0FwMHZXAGvXbv2P//zP81msyAIaWlpq1atIqLt27fv3bu3ra2tq6trz549O3bsYB0THER7V2/tjTaZjF8eE8I6i03QaVXSJUnHM4twlySAWWVzBXzo0KGrV6/qdDqtVpuZmfnBBx8Q0datWx999NGUlJSkpKTNmzdv27aNdUxwEJeKqkVRjAkLcNGoWGexFRtWRLjpNHWNHRcwLgfAbLK5k7Dmz59/+PDh0dN37ty5c+fOuc8DDqzuRtuNlk6VQh4fGcw6iw1RyGUPblr2t39kn8wqSYkP4XmnGJITYO7Z3BYwwJy5UlFPRMtiFqtVCtZZbEtKfIiXh665vaegvJ51FgCHhQIGJ1Xf1N7c3q1SyCNCFrLOYnN4nrt/41Ii+uBUHganBJglKGBwUpeKqoloeVyoQi5jncUWrYwPCfL36ujWYyMYYJaggMEZ1Te1d/Xo3XWa6FBs/t7UHanRhDs0AMwaFDA4HVEUcwqqiCg6PNBJbvo7PcmxwdJGMG5TCDAbUMDgdGpvtHX39Xu667D5O6Ef3JlIRBlnrpjMFtZZABwNChiciyiKVyrqiCgpNgSbvxMKD14QEuDd1TvwWXYp6ywAjgYFDM6l8lpTa0evu04T6O/NOot9eHDTciL6LLt0YHBowpkBYPJQwOBERFEsKq8loqXRi7H5O0nSRvDA4FBmTgXrLAAOBQUMTqTmemuP3uDprlsS5Ms6iz15+M5Enuc+yy7F6dAAMwgFDE5EGvoqISoYm79TEhboExHsOzA49MWFMtZZABwHChicRUVNY3tXr4tGhaO/03Dvujie5zLOXOnVG1hnAXAQKGBwCsNHfxMx9NW0hAcviAj2NZktOB0aYKaggMEp1N5o69EbNGpV6KIFrLPYq3vXxRFRdkE1rgkGmBEoYHAKeSXXiCgmLEAmw8/8NIUHLwjy99IPGC8WXWOdBcAR4MMIHF91fUtXj95Fo4oJX8Q6i33bvD6eiE5mFQuCyDoLgN1DAYPjk05+josIxNHfWxQfHrDId15rZ19uaR3rLAB2DwUMDq6prbu9q1elkC9Z7M86iyO4IzWKiE5mlWAjGOAWoYDBweUVVxNR1JIAlULOOosjSI5d7DPP9XpzZ1FlA+ssAPYNBQyOTK3zbG7v4TguEpu/M4TnuXvWxRERrkcCuEUoYHBkQdGrRVEMWeSjc9GwzuI4kmODPd20VfWtlbUtrLMA2DEUMDisvoEhn8BIIoqLCGSdxaEo5LK71sQS0SeZhayzANgxFDA4rNLaTo7jA3y9vD3dWGdxNGuWh+m0qsralrrGDtZZAOwVChgc08DgUFF1OxEtjQpmncUBKeSy9SsiiOh4ZhHrLAD2CgUMjul8QbXJLHS31fvN92CdxTHdnhKlVSuLKhsaW7tZZwGwSyhgcEzSObpNNThIOVu0aqW0EXwiq4R1FgC7hAIGB1RQfr2rd0CrVnQ2VrPO4sg2rIhQyGUXi2qwEQwwDShgcEDSgcmlYd4W8xDrLI7MTadZGb+YiL64UMY6C4D9QQGDoymqbLje3KlVK6OD57HO4vik65GyC6q7egdYZwGwMyhgcDT/PHOFiDamRKoUuPXCrPOZ57o8OkgQxMycCtZZAOwMChgcSl1jR01Du1atvD0linUWZ3FHajQRnblcOTCIHf4AU4ACBocinfy8KiFUq1ayzuIsQgK8w4MXDAwOnS/AKW8AU4ACBsfR3N5TUH6diKQzg2DO3L0mlogycypMZgvrLAB2AwUMjuNcXpXJbIkPDwjy92KdxbnEhPkH+Xu1dvZdKq5lnQXAbqCAwUEMDA5l5VUR0V1rYlhncUa3p0QS0ekL5YIgss4CYB+mXMBy+ci7moeGhs5QGIDp++JC2cDgUHjwgrBAH9ZZnFFy7GKfea7Xmzur6ltZZwGwD7e6BdzR0dHV1TUjUQCmzWS2SJfB3LsujnUWJ8XznHQ6dMaZK6yzANiHkZuz480qlxORxWKx3gj29PRsb2+f+VzgEEwm06uvvjoHCxogN73oLaehw+/8D9HXu0Cbm5uHhnBhzNxZlRB67HRBWU1Tc3uPr7c76zgAtm4KBWw2m4lIqVTiQw0myWQy/erXv972rz+b7QVxnn4kJ7O+7YahZ3hiTc31IaNxthcNwxRyWWpC6Kns0pNZJVsfSGUdB8DWTaGAJWhfmBKFXP6vu16Y1UU0tXV/+mWuRq165KHHFfJvR7/64uTxirLiWV00jHDPurivLldeKKr5/sYETzct6zgANm3Kx4Dff/99Nzc3juPk31AqMeIBsFRYVktEMWEB1u0LTGjVyuTYYEEQT2bhTx+ACUy5gLdu3Xr48GFRFM3fwDYxMNTR3XejpVMhl0UtCWCdBYiINq9fqpDLLhXXGofMrLMA2LQpFzDP83feeedsRAGYhpLK66Iohgf7qRRTPp4Cs8HTTZsQuUg/YDyVXcI6C4BNm3IBv/rqq7/+9a9nIwrAVA0aTdcaWjmOiw4PZJ0FvrUxJYqIzhfUYGRKgHFMuYB/8Ytf/Nd//ZfcCo4BAyulVddNZkv4Yj93nYZ1FvhWSIB3SIB3R7deGpsMAMY05QI2j4JjwMCE0WQuqbzOcVx8ZDDrLDDS2qRwIjp9oQwjUwLcDMaCBntVVddsNJkXLpiHzV8blBwbrFUrWzv7ymqaWGcBsFHTGQvaGsdx2AUNc89iEYrKaoloaVQw4ygwFoVctjElkohO4HokgJu41V3Q27dv/8c//jGzmU6cOJGQkKBWq0NDQ//2t79JE9PS0kJDQ0NDQ9PS0kI83VsAACAASURBVGZ2cWCPGpo7+g1GHy83v/kerLPA2G5PidKqlZW1LZW1LayzANiiW90F/dZbb/3gBz+YkSiSixcv7t69+9133x0cHDx8+HBmZiYRHThw4MiRIzk5Ofn5+RkZGQcOHJjBJYI9yiu5RkRxEUGsg8BNadXKpNhgIjpzuZJ1FgBbdEsFLAjC8ePHZyqK5LXXXnvrrbdiY2OJKDExUera9PT0V155xcvLy83Nbd++fenp6TO7ULAvTW3dHd19Xh6uwQvns84C47kjNZrnudzSutbOPtZZAGzOLR0DViqVTz311LvvvjuDgU6dOlVYWOjn5xcfH//ll19KE/Pz81evXi09TkxMzM/Pn8Elgt0pKL1GREuCfTmOY50FxuMzzzUlPkQQxH/iHoUAo0x58CDpnkizp6+vLzc3t6ioyN3d/Wc/+xkRbdiwwWAw8PzXfyvwPD/iwqcBg+HQ0e8ch9ZqcFqsw+rRGxpbuzRqVUTIQtZZYGJrk8KzC6ovFdf+8O4krRonbAJ8y+ZG79NoNO+88470+E9/+tOKFSsKCgo0Go0gCFIHC4Iw4rxrrUbzxKMjjkNz+999b44Sw9y6XFQlimJUqD9uvWAXQgK8w4MXVNa2fHGh7L71S1nHAbAh0zkG/MADD0g3RPLw8HjggQdmNtDKlStzc3OH/+np6UlEycnJZ8+elabk5uYuW7ZsxLMUI9ncHxYwI/oNxtobbTIZj81fOyL17ukL5QODGLQH4FtTLuDw8PCHH364vb1dFMXW1taNGzfGx8fPYKCf/exnu3fvbmtrGxoa+vnPf753714i2r59+969e9va2rq6uvbs2bNjx44ZXCLYkSsV9aIoRi72d9GoWGeByQoPXuDr7T4wOHS5uJZ1FgAbMuUCvnr16hNPPCHtBFYqlbt37y4tLZ3BQA899NDu3bs3bNgQFBQUHh6+YcMGItq6deujjz6akpKSlJS0efPmbdu2zeASwV4YTeay6gYiCg/xZ50FpuauNTFE9Fl2KUamBBg25QKOiop65513BgcHiWhwcPD3v/99dHT0zGZ69NFHi4uLm5qadu/ePTxx586d1dXV1dXVzz777MwuDuxFSWW9xSKEBfl5ebiyzgJTkxIf4jPPtbWz70JRDessALZiygVcWlr60UcfeXt7y+VyHx+f7OzsoqKi2UgGYE0UxYqaRiKKi1jEOgtMGc9zq5eHEdFZDMoB8I3pnKz04YcfzngOgPGVVt/oNxj95ntg89dOrUsKP5lVUtPQXlnbEh68gHUcAPZwNySwD5U1jUQUGx7IOghMk1atlG7P8ElmIessADZhagUsl4/cYsatkGAO1De1d3T3ues0gf7erLPA9K1ZvoTnucralub2HtZZANibQgHfcccdGRkZIyYeOnRoxi8FBhghr/gaEcVHBmPsSbvm6aZNiQ8hopNZJayzALA3hQI+e/bsxo0bR0zcvHnz559/PqORAL6jqa27vatXpZAHL/JhnQVulXQ90oWimq7eAdZZABib2i7o4QGZrafM9ujQ4OSKK+uJKCZ8kQoDnNk/X2/38OAFgiBm5V1lnQWAsSkUcHBw8NGjR0dMPHHihJ+f34xGAvhWR3dffWO7TMbH4PQrR4GRKQEkUyjgvLy8Rx555L//+7/1ej0RDQwMpKWl3XfffTk5ObMWD5xdWfUNaexJbP46jPDgBSEB3gODQ2dwTTA4tykUsFarNRqNp0+f9vf3l0bheP/993t6eubPx03RYVYYBo3Vdc0cx8VHBbPOAjNpbVI4EZ3Lq8LIlODMprZVoVQqMQoHzJnC8nqT2RLo541bLziYlPiQf565Io1MmZoQyjoOABsYiANslNFkvnqtkYiWxy5mnQVmGM9zd6RGE65HAueGAgYbVV7dYDSZfbzcvD3dWGeBmZcUG6xVK5vbeyprW1hnAWADBQy2yGIRSq82EFFcRBDrLDArMDIlAAoYbFH19ZZ+g9HTXRe8EKf4OazbU6IUclllbUtNQzvrLAAMoIDBFn2z+RuIsScdmFatTI4NJtyjEJwVChhsTn1Te3tXr7tOsyTIl3UWmF33rIvjee5CUU1rZx/rLABzDQUMNqek8joRhYf4Y/PX4fnMc02MDhIE8bPsUtZZAOYaChhsS1ePvrG1S6WQR4YGsM4Cc2FdUjgRXS6uxciU4GxQwGBbrlTUi6IYtSQAY086ifDgBWGBPhiZEpwQChhsiL7fcLWumeO4KGz+OhNpUI4vLpSbzBbWWQDmDgoYbEhpVYMoikuCfDH2pFNJiFzkM8+1V2+4VFzLOgvA3EEBg60YNJrKqm8QUXwUBt9wOnetiSWik1kluD0DOA8cZgNbUdvQKt16wcPVhXUWuCX/8R8vHZ3iXVt4mTxl80+b22nNHQ+0N1TcYoD9+w+uWZ1yiy8CMNtQwGATRFG8UlFHRHGR2Py1e01NTXfc++D6TfdM6Vm1TT1VDd2r735sRbTfrSx97y+erW/quJVXAJgbKGCwCVfrmnv0Bm9PN7/5HqyzwAzw8vYJXhw2paf4+pvqms/19g+5ei7w8nCd9qLVas20nwswl3AMGGxCYek1IoqLCGQdBJhRqxQRIQuJqKC0lnUWgLmAAgb26m609egN7jpNyCIf1lmApdglARzH1d5o0/cbWGcBmHXYBQ3s5ZfWElFcRBDGnpwpoigKgmAymZisUkEUpvdEnYsmNNC3qq6poLxuTWLkzKYCsDUoYGBMuvWCWqUIxa0XZk7+5QsXs8+89/ZfmCxdqVC+8FLC9J4bF7Goqq7pam1TUmyoWqWY2WAANgUFDIwVlF4jouiwAIVcxjqLQ3nix7ueff4/mCz6Xx64fdrP9fJwXbhg3o2WzoprN5ZGBs9cKACbg2PAwFJ3X39rR69MxkeHLWKdBWxFfGQQEZVebRBFDMoBjgwFDCwVldUR0ZJgP+xshGELF8zzdNf1G4xX65pZZwGYRShgYEa69QIRxUVg8A34DumCtKKyOmwEgwNDAQMz0q0XghbOd9dh5AT4DumGHN19/debMaYVOCwUMLBhGDRKt17AiTYwGsdx0kawdI4egENCAQMbJVUNJrPFb76Hj5cb6yxgiyJCFqoU8taO3q4ePessALMCBQwMmMyWq9eaCLdegJtTyGVRSwKIqLC8nnUWgFmBAgYGSquu9xuMnu66hT7zWGcB2xUVGsBxXHV9c48eI1OCA0IBw1wTRbGyppGIlscslsnwEwg35aJRLQnyFUWxtBIbweCA8PEHc03aoNG5aIIXzmedBWxdXEQgx3GVtU2DRhPrLAAzDAUMc628upGIosMCcOsFmJCnu26Rr5fJbCm+io1gcDQoYJhT9U3tze3dLhpVVOhC1lnAPkhn6pVdbTCZLayzAMwkFDDMKemyzpjwQNx6ASZJulbNaDJX1NxgnQVgJqGAYe50dPe1dvSqFPKIEH/WWcCeSKO1FOP2DOBYUMAwd/JKpM3fRSoF7oMJUyCNV6rvN1TX4/YM4DhQwDBHevSG+sZ23HkQpiciNICI8kuuYSMYHAYKGOaI9NEZudgfdx6EaYgI8Vcp5D16bASD47DdAi4vL9dqtcP/TEtLCw0NDQ0NTUtLY5gKpqeju6+6vlkm4+OjgllnAbukUshjwhcRUXFlA+ssADPDRgtYEIQf/ehHBsPX488dOHDgyJEjOTk5+fn5GRkZBw4cYBsPpqqyplEUxUA/bxeNinUWsFdLI4PVKkV7V299UzvrLAAzwEYL+KWXXnryySeH/5menv7KK694eXm5ubnt27cvPT2dYTaYqh69ofxaI8dxiXEhrLOAHZPJ+OiwACLKK8Y9CsER2GIBnzt3Ljc3d/fu3cNT8vPzV69eLT1OTEzMz89nFA2mI7/kmsUiBC+c7+HqwjoL2DfpCvL2rt6mtm7WWQBulc1dDaLX63ft2nXy5EnriQaDgee//luB5/mhoSHrrw4ajZ9/+ZX1FJUK+zlthcbF7VpDC8dxSfFhrLOA3ZOOBBeU1uYVV39vQyLrOAC3xOYKeNeuXXv37l2wYIH1RI1GIwiC1MGCICiVSuuvKhWKZUvjrafIZHxNbd0cpIUJJay932IRwoP93HUa1lnAEcQuCSypvN7U1t3c3u3r7cE6DsD02dwu6Lfffvvhhx/mOE4aqV/6f3Jy8tmzZ6UZcnNzly1bZv0UnucX+vla/+fr4zP3yWG0fsNQSOwqjuOWRi9mnQUchFqliIsIJKKiMvyRDfbN5gpYtCL9k4i2b9++d+/etra2rq6uPXv27Nixg3VMmJQvLpTzvCx8MTZ/YSZFhy2Syfj6pvb2rl7WWQCmz+YKeExbt2599NFHU1JSkpKSNm/evG3bNtaJYGId3frswmtEFB8ZzDoLOBS1ShG52J9wOjTYOZsuYOsx53bu3FldXV1dXf3ss88yjASTl5lTYRwy11XkYfMXZlxCdDDHcdLdLVlnAZgmmy5gsF9dvQNfXa7keS4v8wPWWcABadSqmCWLiCj3SjXrLADThAKGWXH6QplxyLwiNkjf08E6CzimpZGBMhkvnQ7NOgvAdKCAYeZJm79EtGZ5KOss4LA0alVYkC8RXS7CRjDYJRQwzLzjmYXGIfPK+JCFPrhME2ZRclyYQi5rbu9uaMaOFrA/KGCYYV29AxeLrvE8d//GpayzgINTqxQRIQuJqKC0lnUWgClDAcMM+/h0gclsSYkP8fLQsc4Cji8hKljaCK6qa2KdBWBqUMAwk5rbey4U1Sjkss3r4yeeG+CWDQ+MVVheb33hIoDtQwHDTDqeWSQI4rqkcGz+wpyJDlukkMu6evRX65pZZwGYAhQwzJi6xo7c0jqFXHZ7SiTrLOBEhjeCLxVVYyMY7AgKGGYMNn+BlaWRwWqVwjBoxEYw2BEUMMyMusaO4qobCrns3nVxrLOA05HJ+OiwACK6VFTN8TLWcQAmBQUMM+PwicvS5q9Oq2KdBZzR0shgnYvGMGhcEBzLOgvApKCAYQaU1TRV1bdq1Uqc/AysyGR8QmQQEfmFJQo4Egz2AAUMt0oQxMMnLhPRHanRWrWSdRxwXhEh/l4ergqVtqnTyDoLwMRQwHCrsguqG1u7vTx0d6RGs84CTo3juJRl4UR0rWWgV29gHQdgAihguCUms+V4ZiER3b9xqUKOk1+AMb/5Hv3drRaBvrhQzjoLwARQwHBLzlyu7Ood8PfxSI5dzDoLABFRfclZIjqVXdLRrWedBWA8KGCYPuOQ+bPsUiK6f2MCz3Os4wAQEfV1Nnm5KgVBzMypYJ0FYDwoYJi+jDNXunoHgvy94sMDWGcB+FbIAg3Pc59fKMNGMNgyFDBMU1fvwBcXyojokbuTsPkLNkWrlt2WFC4IYsaZK6yzANwUChim6XhmoclsWR4dFBbowzoLwEh3rYlVKeVZeVXXmztZZwEYGwoYpuN6c2d2QTXPc/dh5A2wSZ5uWum6uKOn8lhnARgbChimI+NMsSCItyWF+/t4sM4CMLa718R6eejKaprKappYZwEYAwoYpqyg/HpBeb1KKb9rDQbdBdulkMuksVH/9o9sk9nCOg7ASChgmBpBEI+eyhUE8ZG7kz3dtKzjAIwnNSE0LNCnq3fgzOVK1lkARkIBw9Rk5V1t7ezzmeeamhDKOgvAxKSN4GOnC7p6B1hnAfgOFDBMgX7A+NHn+US05d4VuPQI7EJUiF9UiJ9xyPzx6QLWWQC+AwUMU3A8s3BgcCgmzD8mzJ91FoDJ2nJvMhFlF1TXNLSzzgLwLRQwTFZNQ/tXlyt5nntw0zLWWQCmwNfb/c7UaCI6cuIS6ywA30IBw2R99HmeIIh3psYs8p3HOgvA1Hx/Y4Knm7amof1iUQ3rLABfQwHDpJy5XFlZ2+Km09y1JoZ1FoApU8hl0p6bQxmX9ANG1nEAiFDAMBkDg0PHThcQ0SN3J2nVStZxAKZjZXxIVIjfwOAQBogGG4EChol99Hm+fsAYFuiTGB3EOgvA9D24aRnPc1/mlNc1drDOAoACholU1bdm5V0l3PUI7F+Qv9emlChBEA+fuMw6CwAKGMYlCOJHn+cLgnhnanSQvxfrOAC36p51cTqtqqq+FWNjAXMoYMe3cOFCfrpWbHyoqr51cKDvqUfumsbTdTqdyWxmvQIAvqVVK7fcu4K+ObDCOg44NTnrADDrBEE8/sVlb58FU31iv8H40cmLRpP5no0pu7YWTmPR3d2d39uQOI0nAsye5NjgvNL6vNK6o6dytz6QyjoOOC9sATsHbjqyLpcbTWZfb4+QRQum9QIcx+GYMdiif7k3WaWUZxdUl1Q1ss4CzgsFDGOru9HW0Nwhk/FrkiPRo+Bg3HSaBzctJ6LDJy7jToXACgoYxmAYNGblVhDR0sggD1cX1nEAZt6GFRFRIX7N7T24LBhYQQHDGHJLrhkGjZ7uurgIXPgLDmvrA6kqpTzjzBXcpAGYQAHDSA3NHRU1jRzH3bYiSiGXsY4DMFs83bSb1y8loveOX8SOaJh7KGD4DlEUs3IrRFGMC1/k7enGOg7A7LozNTos0Od6cyd2RMPcw2VI8B2Xiqr0/QZ3nSYxNpR1FoDpGBjoL7lS+IWnepLzL/YSrzVw/zx7xdTX7KlT3HqAtWvXKpUYMh0mhgKGb3V0912pvM5x3G0rY2Uy7B0Bu9Te3nr0yHunvzg5+af4h6d4B8Ye+6qs+vInonBL+6Jzcy7kFpXFRYbcyouAk0ABw9csFiHzYqkoignRwT5e2PkM9krGy1546VcJy1dM/ikms+XYZ5eI6F+e2ZeSsORWln73uoShIRxOhknBVg58La/kWleP3sPVZVnUYtZZAOaUQi7bsCpGJuNLrl5v7ehlHQecBQoYiIhaO3qLKuqIaN2KaOx8Bifk5eGaGBsqiuIX2UVGEwYwh7lgcx+1GRkZt99+u1ar1Wq1TzzxRFtbmzQ9LS0tNDQ0NDQ0LS2NbULHI4rimZxSURTjIwKx8xmcVlz4Il9vj36DMe9KNess4BRsroDfeeedZ555pre3V6/X33333U888QQRHThw4MiRIzk5Ofn5+RkZGQcOHGAd06FcLKzq7uv39nTDmc/gzDiOW5McqZDLSqoayqtvsI4Djs/mCvj999//4Q9/KJfLeZ5//PHHT58+TUTp6emvvPKKl5eXm5vbvn370tPTWcd0HHU32oor6xVy2YZVOPMZnJ2Hq0tKQjgRXSqq6jfgZoUwu2z6A7e4uDg+Pp6I8vPzV69eLU1MTEzMz89nmstxGAaN2XkVRJQUH+au07COA8BeRIi/33wPo8n8RXaRKIqs44Ajs93LkAYGBp5++uk33niDiAwGA89//bcCz/NDQ0PWc5pMprzC74xio1DMwNX0zuCrnLJ+gzHQzzs6dCHrLAC2YuOq2A9PXWrt6M0vvbY8Blf0wmyx0S3gjo6O++6778UXX1y7di0RaTQaQRCkLwmCMGqUGU6lUn7nPwxDMwmXi6sbmjvUKsW6FdG44SDAMI1atTY5kojySq7daOlkHQccli1uAZeWlv74xz/+wx/+sHLlSmlKcnLy2bNnb7vtNiLKzc1dtmyZ9fwKhTwhLnbEi2RduDg3ae3UjZbOwrI6juNuT41Xq7DDAOA7Av284yMCiyrqMy+WPnRnskatYp0IHJDNbQGfOHFi165dH3744XD7EtH27dv37t3b1tbW1dW1Z8+eHTt2MEzoAPoNRmnQq7jwRX7zPVjHAbBFyfFhXh6uhkHjVzllOBgMs8HmtoDvueceIvL39x+eIori1q1b+/v7U1JSiOj555/ftm0bs3z2z2IRvjxfbBg0Bvh6JceHsY4DYKM4jlu/MvrjLy43NHcUltUlRAezTgSOxuYK+GZ/ae7cuXPnzp1zHMYhnS+obG7v9vJw3bAqFod+Acbh6a5bkxT15YXiy8XVvj4evt7YXQQzyeZ2QcOsqqhprKhpVMhl61dGqxQ29+cXgK0JDVwQGx5IRGdzSgeNJtZxwKGggJ1IV4/+QkGlKIrrVkR7uutYxwGwDyuXhvnN9+jRGzIvluBgMMwgFLCzMAwaT5wpMJktSyODFwf4sI4DYDc4jtu0ZqlGrWpo7jiXV8E6DjgOFLBTsAjiZ+eK+g3GAF+v5TG42yDA1KgU8rvXLVWrFOXVNyprm1jHAQeBAnYKRZWNrR29Hq4uGPAZYHq8PFzXJkUR0dlLZc3t3azjgCPAZ7HjC19+e31zl0ohv2PtUpx4BTBtQQvnJ8WGiqL4+bmi7r5+1nHA7qGAHVxRZUN44u0yntuwKha3WwC4RQnRwWFBfoNG0+dZV3BSNNwiFLAjq6pv/cvhMzwviw3zC/D1Yh0HwBHctiLK19uju6//n1/lm8wW1nHAjqGAHdb15s43D2WazJar+ZnB/vNYxwFwEBzH3bF2qZeHa0d33+fnitDBMG0oYMfU1Tvw5/e+1A8Yk2ODKy6fYh0HwKGoFPKNqXFqleJGS2fWZYwUDdOEAnZAvXrD7w+e6uodCAv02fpAqiDgL3SAGeau09y9LkEhl1XXt2TllrOOA3YJBexoBEH8nw/Otnb2+ft4/HTLeoVcxjoRgGPy9nS7PTVOJuMrahovF1ezjgP2BwXsUIxD5tcPnqqsbfHy0O3+0e06LW5iCjCLAny91iVHcxxXUFpbUtXAOg7YGVwV6lAO/iO7qr7V0037wlN3eLppWccBcHyhgQsGh0zn8yrO51XIeWzSwBTgx8VBCIL41uEzeaV1bjrNi9vv8vLAvRYA5khMWIA0wuvZy2WLY1JYxwG7gQJ2BIIgHvxHdl5pnVat3P2jjWhfgDm2PCYkKTaUiBI3/LC8to11HLAPKGC7ZzJb3jyUebGoRqtWPvfkpkW+uOQXgIGE6GCpg8/kVWflVbGOA3YABWzfTGbLXw6fKapskNo3yB/DXQEwkxAdXJpzkoje+fg8OhgmhAK2YwODQ394+3O0L4DtKM05lRy9iIje+fh8xpkrrOOATUMB26teveH3Bz+rqm9102nQvgC2Y1nkwgc3LSOiY6cLjp7KFQSMkwVjw2VIdqmqvvWtw2d69QYvD91zT27ymefKOhEAfOvuNbE+81z3f3juVHZpj37wie+nYEgcGA0FbH9Kqhqluyws8p23+0cb3XCTQQDbszw6SKdVSydIdnTrn35kHX5VYQTsgrYzX+ZUSO0bHrzg50/dgV9pAJsl/ZJ6ummr6ltf/UtGXWMH60RgW1DAdkMQxHc+Pn8oI8dktqxLCt/9o9u1aiXrUAAwnkW+8/buvC8kwLurd+C1/SfzSutYJwIbggK2DwODQ68fPJWVV8Xz3MN3Jj6+eSUOKQHYBa1a+fOn7lweHWQyW946fOaTzELWicBWoIDtQE1D+2v7T0onPD//5B13pkazTgQAU6CQy55+ZN3m9fFEdDyz6M/vfWkcMrMOBeyhgG3dxaKaP7z9WWNrd5C/10s/uTc8eAHrRAAwHfetX/rTLeu1amVRZcOrf8lobu9hnQgYQwHbLuOQ+e/HLx78R7ZxyHzvurh/33EPbnAEYNcSIhf917PfDwnwbm7vefUvGReLalgnApZwGZKNqmlof+fj842t3W46zb/+YC02fAEcg5tO88sd9xw7XXAiq3j/h+fySusf37wSlzM4JxSwzTEOmY+dLvgyp1wQxKgQvx0/WKvTqliHAoCZdP/GhJgw//QPzhaUX6+qb936QGp8eADrUDDXUMC2paSq8VBGTmtnH89zD25admdqDM9zrEMBwMwLC/T5r2fvT//gbFFlw5/f+zIhctHWB1JxbaFTQQHbCumIr3RMyGee608eWYcbCwI4NpVSvuuxDVl5VUdP5RaUX6/8w0cPblq2ZvkS/NntJFDANqGosuG94xe7egd4nrszNebedXEqJb41AE5hzfKw+PCF+z88V1bT9PfjF89cvvrI3Uk47cMZ4FOescbW7mOnCwrKrxNRkL/X45tX4r5GAM5GuqdZQfn1v/0j+3pz5+sHT61LCr93XRwufHBsKGBmevWGY6cLsguqBUH0dNN+f2NCcmwwxrcCcFoJkYvCn3vwiwtlJ7NKzlyuvFhUs3n90tuSwrE/zFHh+8rAwODQZ9mlX1woMw6ZeZ7bsCLiwU3L8TsGAFq18r71SxOjgz76PL+osuHoqdzMnIof3Lk8ITIQB4YdDz7055RxyJxdUJ1x5kqv3kBEybHB39+YgLv5AoA1fx+PXY9tqKxtOXzi8vXmzrcOnwny97ojNTo5Nph1NJhJKOA5MjA4lJVX9c8zVwYGh4goJsz//o0JONwLADcTHrzg5We+d7Go5nhmUV1jR/oHZ09mldyRGpUcuxhbw44BBTzrmtt7zuVVZeVVDVfv3WticYojAEzGyviQ5NjFuaV1H58uuN7cuf/Dcx99nr9+RcS6pHBcNGzvUMCzqKSqMSuv6kplg8lsIaKEyEV3rYkNCfBmnQsA7AnPc8mxwYnRQdkF1Zk5FdebOz/6PP9kVsmqhND1KyJwDMt+oYBnnn7AeKm49vSFstbOPiJSyGWpCaF3pEb7+3iwjgYA9ornuTXLw9YsDyuqbDiZVVJV3/rFhbIvc8rjwwNWLw+LDVuI/dJ2BwU8Y0xmS0lV4/mC6pKqRmmT18tDtzJ+8YYVERhpHcBJ6PW9qcmxRLPeha6ePuFL1yxZurag/HpB+fWBvq7q4gvtN67mX8p20Shme+m25siRIz964gkSmQXY/fz/89pvfzXVZ6GAb5VxyFxSdeNi0bXh3uV5LibMf2X8YpwrAeBseJ4//MlX87zmz83iLIJQ39RRXnWjjShu1T1E97zy5sexYf4r40Oc6kQTi8WyfuNde1/9I5OlH/zL/+nq6Z/GE1HA0zQwOHSlsuFK5Y2Sqkbp7CoiCgv0WR4duDI+BPcvAnBaSqVSqZy706MiFi+MWLywu6+/tLL+ckEJEWXlVWXlVWnVyrjwgJXxi8ODkRgbUwAAEZZJREFUFzjDCD+8jJ/L1W5NJpebTaZpPBEFPDVV9a1lNU2VtS1V9a2C8PX+jvDgBXHhASnxi7GrGQCY8HB1WRoR8J87H7yYX1HX2H6+oLq1s+9iUc3Fohqe5xKjgyJD/OLDF+IzyqaggCcwMDhU19hR19hRUtVY19hhHDJL03meiw8PWBG/OCzQB+O1AoCN8PZ0jQnzu3ddXE1D++Xi2rKapsbW7kvFtZeKa4nI000bFx7g7+MRFjgf91tjDgU8hl69oaK2pbK2paG583pzl3RkV+Lppg0L9EmKDY4K8cPgkQBgs0ICvKWLHnv1huKqxtKqxoralq7egTOXK6UZdFrVIt954cELwgJ9Anw9b/GqYqPRWFdXNwO5p6WpqUkU2J2CNV2oEDKZLW2dfdebOxuau260dl9v7pLGiRzm7+PxzY/pfJ95bjivCgDsiJtOk5oQmpoQSkTXmzuvVN6oa+yorG3RDxjLaprKapqk2TzdtIt85/n7eAT4ei708fD1dp/SZ11xcXFq6uqFAQGz8h4m0tHetixpFZNF3wrnKmBBEFs7extbu3v0gy3tPc3tvT16Q1tnn/U2LhH5zHMN8J23yNczwNdzke887GEGAMewyHfe8J7n5vaextbu681dja3ddY0dXb0DXb0DRZUN0ldVSrlOq/b1dlvo4+GiVfn7ePh6u+u0qnE2lMMjIvcfypiLtzHK/351T0vTDSaLvhV2U8BpaWmvv/46Eb3wwgs7d+6cxiu8fvBUZW3L6Ok6rSrI30unVfn7ePj7eESF+M34OcxXrlzp6emZ2decPLPFzGrRADBnBMFisVguXjg/z30KZ1p5KckrQB4XsKCzz9jTb+rqGxocsvQOmLr0Qx3d+o5ufUlVo/X8Lmq5TiPXquSuWrlGKVMrZSqFTKOS3ai/ZrEIM/2eHJx9FPCBAweOHDmSk5OjUCgee+wxjUazbdu2qb6ITqumb3azuOnU8+e5SvuW52ADd9euZ1va2l1d3WZ7QWPS66dzgRoA2JdBg8E4aPhf/2sPz83MYTKVi7vWzVvt4ilTqNUu7moXD6VG1z9I/YNj/k2vWP3Q84c+zdZpVCqVQq1SuGhUWrWKl/FatVImkxGRVqOScSST8Ro1LtQkspcCTk9P/+1vf+vl5UVE+/bte+6556ZRwE89kPqvP1jL5AiuKIo///dXliezOURxW3I4k+UCwBxTKJVv/e3D2Xt9URS7e/sHh8w9vf0Dg8Z+g9FgGBocGhoYNOn7B3iZXN9v0PcbJn4hIiJSKeQKpULGkUatkv5mcNFqeI6kziYipUKuVH5nVC8XjYrn+eF/KhUylUJORLxCrVC7jF60QqmQZrBNtpvMWn5+/urVq6XHiYmJ+fn51l+1WCx11xusp8hlY1x1zvak5bzLF7q7O9ksWxTPnfnczZ3BSNT9+j5REE9/9uncL5qIrhTmGgwDrJZeX1vT0d7Kaukd7e1116pYLd1gGCgrKXTR6Zgs3WIx5+Wc7+xoY7J0IsrK/FznxmB3V093l2AR5vibLifSEemUdKPwwtkzp3/6/H9aBM4scBaRE0QyW4iIMwucdIKyWeCISBTJInJEZDSZjSYzEfV8e95r9/RiuAWluAXRoU+zp/9G+OmfRG1yCeW6y6fxRK6wsDA+Pn7aC54bHMeJ4rdrRy6Xm83f7gMxDg2dOXfeen6lUlleefXpbU/OXcRx/cdLL+dcLmC19M6OtjkbGG8EQRA6O9u9vX2YLH3QYLBYzC46NveK6enp0mpdFAo2Q/O0tTZ7+yzgZn9E4jEx/JEjou6uDg9PZnfa7uho9fJi8wMvCJaurk4vRmveYBgQRMFFO4W/umQKFc/LOZ6XKTVERBwnV2qJiJfJZXIlEcnkKl5mteHE8XLldw5v84qvZxAEgef40T/vI19h1gS59r/0wjPWU9468Pb4HVRUVGQfW8AajUYQBGnPgyAII8YbUymVd2y4bcRTyiuvzl2+ifz6V/+v0WSZeL7ZYbEIIpFcxk886ywwWwSOIxnPZukms0XG86yuHBsyWRRynpuhA3JTZRyyqJRsBiAURXHILKgUbJYuCKJZEJVyNj9y+HVj9etmNFmUt/Dr1t03INzClcTz3F2m8Sz7KODk5OSzZ8/edtttRJSbm7ts2TLWiaaG5zmNyj5WtYNhu9qdeem4dM8J2fUPvEbF4KiBfbTC9u3b9+7d+8EHH8jl8j179uzYsWPCp6iUyrcOvD0H2QAAAEZwdZ14m9g+Cnjr1q39/f0pKSlE9Pzzz0/mFOinHt9i/c+vzp1fMN87MnzJbEV0XOlv/33b41tkY53XBuOoqa2rvlY7+uAITOjkF19GLAkLDlzEOoidGTKZ/v7/f7DtR//COoj9KSmv6OrqXrNq5Rwv1z4KmIh27tw5vfE3AAAAbBCbY/UAAABODgUMAADAAAoYAACAAfsYiOPWDQwY5HLZiAuIYTK6uns8PdxZp7A/QyaTacjk4oLrcaZM39+vUioVCsXEs4IVURR7ens93PHbOmXGoSGLxaLVTOEmFrfObgbiuHVa7ZyuWUeC9p0epUKhRIVMi85lOmMaAMdxaN/pUTHaNsMuaAAAAAZQwAAAAAyggAEAABhAAQMAADCAAgYAAGDA8Qs4LS0tNDQ0NDQ0LS2NdRbbZTabf/Ob34y4k9eYqw7r01pGRsbtt9+u1Wq1Wu0TTzzR1vb1TeCx6sb38ccfr127Vq1Wa7Xaxx9/vKWlRZqO9TZ55eXlWu23F7lh1U2IG0WaznLVFRYWio5r//7969evb29v7+np+d73vrd//37WiWyUSqX63ve+R0TDU8ZcdVifI2zZsuXw4cMmk8lisbz77rt33XWXiFU3CY899tixY8csFovRaHzppZfWr18vYr1NhcViSUxMHP6FxaqbDOvPt2EMV11hYaGDF3BqauqZM2ekxzk5OampqWzz2DjrH9AxVx3W5/gUCoWIVTd1WG9T9ctf/vKPf/zj8C8sVt1kjFnADFed4xewRqOxWCzSY4vFotFo2OaxcdY/oGOuOqzPcVy5ciUxMVHEqpsKi8XyxhtvSHsOsN4mKSsra9OmTaLVLyxW3WS4urq6uroqFIqQkJCDBw9KExmuusLCQgcfCctgMPD8/23vbkKiavs4jl+T06QZQ6OVykC+wZRgbwuJoDccoSQNw1scF0FuCk0IF5EUaiDGSJGLUhCC0hILicrn6VUNo3AjEjMLTdvcFWa+zAyaiZx05l6ch/NMOZlG3ZeO388ijv855z+Xf9Kfei6d/93nXrFihaIoctezhAQcHfP8kcnJyRMnTlRXVwtGN2+hoaHT09NGo/H169eCuc3PxMTEyZMnnz596l9kdPMxPj6uHrx79+7UqVNxcXH79u2TO7og34QVFhbm9XrVY6/Xy9+Cnr+Ao2OeAblcrszMzNOnT+/Zs0cwunmbmpqanJy02+02m00wt/k5efJkWVlZVFSUf5HRLUhsbOytW7eKi4uF7NEFeQCnpKS8fPlSPe7u7t6xY4fc9SwhAUfHPGfr6enJyMi4cOFCVlaWWmF082cwGI4fP97d3S2Y2/w0NDRkZ2drm3jVfxndQnm93vDwcCF9dMF9D/jGjRt79+4dHh52u90HDhxgH+DchN894ICjY57fefz48f79+z9+/OhfZHQ/ZbPZWltbZ2Zmvn79evHixczMTB9zWzjtA5bRzYfNZnv69OnMzMzw8HB2dnZnZ6dP6uiCfxOWz+erqalJSEhISEi4cuWK7LUsduLbXYIBR8c8/c3+ilatM7q5PXjwYPfu3SEhIWFhYQUFBWNjY2qduS2I/wcso/sp7X/dtm3b7t27p9Vljc7hcCyX1wMGAGDxcDqdQX4PGACAxYkABgBAAgIYAAAJCGAAACQggAEAkIAABgBAAgIYAAAJCGAAACQggAEAkIAABgBAAgIYAAAJCGAAACQggIGlR30V2LkrABY5AhgAAAkIYCCojIyMWK1Wg8FgtVpdLpda1Ol0zc3NVqtVCNHW1pacnBwaGpqcnHznzh31BI/Hk5GRERoaevDgQY/Ho111//79tWvX7tq1a2hoKGB/l8uVmJioPaTT6bTL4+PjXS7Xjzpr6wGWLQIYCCrl5eXp6emKohw6dKi0tFSrT05Otre3CyHy8vKuX78+NTVVU1PT0tKiPlpaWnrkyJGpqakzZ85UVFRoV3V2drrd7ry8vLKysoD9IyMjN27c2NXVJYR4/vx5eHj4kydPhBBdXV0bN26MjIz8UWdtPcCypXM4HFu3bpW9DAALEPCOr8/nE0JEREQMDw/r9XpFUaKjo91ut3p+X1+fxWIRQlgslvz8/GPHjsXExGjXRkVFffjwwWAweL1es9k8ODioXvXly5fVq1crirJu3brx8fGA/a9evTo0NFRRUZGXl2cymTweT1NT07lz52JiYoqKin7UWVsPsDw5nU4CGFh6dDqdGrezK/4PGQwGRVG+Kw4MDFRXV7e0tBiNxurq6j179ohvEz0kJGR6eno+rdTiwMCA1Wp98+bN+vXrP3z4EB8fPzg4uHnz5vb2drPZ/NPOwPLkdDr5ETQQVEwmk5qUiqKsWbNm9glms/nSpUv9/f12u91ms6nFDRs2zMzM+Hw+n8+nZqRqampKbWUymX7U32w2m0ym+vr6nTt3hoaGpqSk1NfXm0wms9k8R2cABDAQVGw2W1VVlRCisrJSy1d/R48ebWtrE0KYTCav16sWc3Nzr127JoRwOp35+fnayepd26tXr+bk5MzRPzs7+/z582lpaUKItLS0srKyrKysuTsDEA6HwwdgSRFC/KgyOjqampq6cuXK1NTU0dHR2effvn07KSkpJCQkKSmptbVVLX7+/DknJyckJCQhIaGhoUG76u7du+Hh4Xv37tVaBez/9u1bIURvb6/P5+vt7RVC9PX1zd35t84DWHocDgf3gAEExp1a4M/hHjAAAHIQwAACW7VqlewlAMGMAAYQmLoFGsAfQgADACABAQwAgAQEMAAAEhDAAABIQAADACABAQwAgAQEMAAAEhDAAABIQAADACABAQwAgAQEMAAAEuhlLwBY1pxOp+wlLD28giqCAwEMSEacLAhfsiBo8CNoAAAkIIABAJCAAAawADqd7ubNm99V/vQz/tH+gCwEMICFqaqqGhoakr0KYMkjgAEsjN1uLygomF0fGRmxWq0Gg8FqtbpcLrWo0+mam5utVqt6XFtbGxUVFRsb++jRo5KSEqPRuH379p6eHvVkq9Wq0+n0en1iYmJbW9u/9h4BUrALGlgU+v8e6vv7k+xVfGNTXLQlLmp2PSMjo7Gxsbm5OScnx79eXl6enp7e3t5++fLl0tLS2tpatT45Odne3q4ev3//fmBg4NmzZ4cOHXr48KHdbm9pafnrr7/UDNZOu3//fmFhYX9//x989wDZdA6Hg9+CAGRxOp3qB+B/Ohz/7Vhcv2CTuX9bxv7vPznodDqfz+dyufbt2/fixYvIyEi1IoSIiIgYHh7W6/WKokRHR7vdbvX8vr4+i8WiXevfRz3W6/XT09PfPZFW9D9T+E0MWNKcTiffAQOLwqa4aN3+xbXbKOC3v6rIyMjS0tKioqKmpiat6PF49Hq9EMJgMExMTPy/j8Uy9xPNzMyoB/39/eXl5R0dHWNjY1oRCFYEMLAoWOKi5gi8RSg3N7exsbGlpUWrmEwmRVEMBoOiKGvWrPmFnocPHy4sLKyrqzMajWx+RtBjExaAX1RXV3f27FntTZvNVlVVJYSorKy02Wy/0PDTp09HjhwRQpSUlPyuRQKLFgEM4BfFxMQUFxdrb1ZUVHR0dBgMhlevXlVUVPxCw5qamqSkpC1btmzatCk6Otrj8fy+xQKLDpuwAJnYUrRQTAzBwel08h0wAAASEMAAAEjALmhAMl5fD1ieCGBAJm5nAssWP4IGAEACAhgAAAkIYAAAJCCAAQCQgAAGAEACAhgAAAkIYAAAJCCAAQCQgAAGAEACveAv4QEA8K/7B9RuWSFc6w7pAAAAAElFTkSuQmCC"/>
</div>
</article>
</section>
</body>
</html>




<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="SGPlot" data-sec-type="proc">
<h1 class="contentprocname toc">The SGPLOT Procedure</h1>
<article id="IDX">
<h1 class="contentitem toc">The SGPlot Procedure</h1>
<div class="c">
<img style="height: 480px; width: 640px" alt="The SGPlot Procedure" src="data:image/png;base64,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PhU+yWQybd++/d///nffifgk+KCurq7c3NzCwsLAwMCf//znRLR69WpWnwQvL2CVSsXzvPPvGow855uMRuO999775JNP3njjjYRPhU/avn37rl27wsPD+07EJ8EHqVSq/fv3i7dff/31RYsW5efns/okePlBWAsXLjx58qR4Ozc3d+7cuWzzwOQrKirasGHDnj177rrrLnEKPhU+6J133tm4cSPHcRzHEZH4f3wSfNDixYtzc3Odd4ODg4nhJ8G7D8J66623VqxY0dzc3NraevPNN+/bt491IphU//rXv1atWlVfX993Ij4VPo6uHYSFT4IP+uijj5YuXdrc3GyxWLZv3y4ekMXkk1BQUODlm6C3bNnS3d29ZMkSItqxY8dDDz3EOhFMqltvvZWI9Hq9c4ogCPhUgAifBB/0/e9/32azrV692mg0Pv300+JBWKw+CV5+FDQAAIAbKiws9PJ9wAAAAO4JBQwAAMAAChgAAIABFDAAAAADKGAAAAAGUMAAAAAMoIABAAAYQAEDAAAwgAIGAABgAAUMAADAAAoYAACAARQwAAAAAyhgAI/EcZzzCqZOr776qnilW3EGJ7Vaff/997e0tDjnNBqNv/jFLyIjIxUKRVRU1K9+9avOzs5BF2QymZ544gnxdmlp6YYNG9RqtVqt3rJlS1NTkzh9zpw5zoUOk3mYpQD4IBQwgKd6/fXX+005cOBA37vOK4+aTKZHH330nnvuEae3tbWtXLlSr9dfuXLFarWeP38+ISHhkUceGXQpW7dufeyxx4iopqZm9erVGzduNJlMnZ2d69atcz4kPz9/JIEzMjKGWgqAD0IBA3iq+Pj4oqIi593Dhw/fdtttg84pkUhuvPHGr776Srz7hz/8YevWrb/61a+0Wi0RRUZGZmRkvP/++wMfePToUb1en5CQQES/+93vxEulSiQSmUy2efPmTz75RJxNXPF1/p/juKlTp/I873weu90eFxcXGho6ZcqUo0ePuuTlA3g6FDCAp9q+ffvzzz/vvPvKK688+uijQ8184sSJW265Rbz97rvvjvCS4//n//yfO++8U7x96NChLVu2DDOzIAh0bbX7zjvvzM7Odv4oKytr48aNWq1248aNf/nLX0ayaACvhwIG8FRxcXFGo7GqqoqI8vPzIyIioqKi+s7g3Aes1Wrfe++9t99+W5xuNBqDg4MHzjZwEZ9//vmNN94o3jYYDFOmTBlhtoyMjL5byP/85z8//vjjRHTDDTdgDRhAhAIG8GDOnnvjjTd+8Ytf9Pupcx9wZ2fn3r17naWr0+lMJlO/2QZ9/t7eXplMJt4OCAgY+SFUycnJer3+xIkTRPTpp5+mpaXFxcURkUKh6O3tHcUrBPBeKGAAD7Zhw4bDhw+XlJSUlJQsXLhwhI+677779u3bN5I5/fz8rFarePvuu+9+6623Rp7tN7/5jbiF/Pnnn3/yySfFiVar1c/Pb+RPAuDFUMAAnm3z5s233Xbbz372s5E/ZOfOnVlZWc8//3xDQwMRWa3W/fv3DzrnunXrjh8/zXH5YAAABGlJREFULt5++umnX3zxxffff5/nebvdnp2d/f3vf7/f/LNmzRKfk4hWrlxZW1v7/vvv2+125x8HX3311U033TSa1wfgtVDAAJ7t4YcfttvtP/jBD0b+kODg4BMnThiNxgULFshkspCQkI8++shZtH09+uijzkOdU1NTDx06lJWVpVarg4KCzp49u3fv3n7z//Of/1y5cuXq1avFuz/72c9+8pOfiGcxiQ4ePPjwww+P6gUCeCuuoKAgPT2ddQwAcFP33nvvnj17kpKSxvDYioqK9evXl5eXO+8+9dRTH374oUsDAnikwsJCrAEDwHD27duXmZk5hgeaTKaf/OQnfY+F/tOf/jTCfc8AvgBrwADgegsWLOjp6XnppZc2bNjAOguAOyosLJSxzgAAXuj8+fOsIwC4O2yCBgAAYAAFDAAAwAAKGAAAgAEUMAAAAAMoYAAAAAZQwAAAAAyggAEAABhAAQMAADCAAgYAAGAABQwAAMAAChgAAIABjAUNwFJhYSHrCJ4H148B74ACBmAMdTIq+JMFvAY2QQMAADCAAgYAAGAABQwAo8Bx3P79+/tNmeglTujzA7CCAgaA0XnxxRebmppYpwDweChgABidF1544ac//enA6S0tLWvXrlUoFGvXrjUajeJEjuMOHjy4du1a8XZmZmZ4eHhcXNyRI0eeeuoprVY7Z86coqIicea1a9dyHCeTyRITEz///PNJe0UATOAoaAC3UFrZdKWykXWK70iJj0iODx84fcOGDe++++7Bgwd/8IMf9J2+e/fuW2+99Ysvvnj11Vd37tyZmZkpTu/p6fniiy/E29XV1XV1dUePHr3tttv++c9/vvDCC4cOHbrnnnvEDnbO9sknn2RkZJSWlk7gywNgjSsoKMBZEACsFBYWiv8A/3G84PBx9zrB5vZVszes6v/lwHGcIAhGo3HlypUnTpzQ6XTiFCIKCQlpbm6WyWRWqzUiIqK1tVWc/8qVK8nJyc7H9n0e8bZMJrPb7f0W5JzYd07q844BeLTCwkKsAQO4hZT4CG6Vex1tNOjqr0in0+3cufNnP/vZ+++/75zY1tYmk8mISKFQmEym/z5PcvLwC3I4HOKN0tLS3bt3Hz9+vKOjwzkRwFuhgAHcQnJ8+DCF54Z++MMfvvvuu4cOHXJOCQ4OtlqtCoXCarVqNJoxPOcdd9yRkZGxd+9erVaLg5/B6+EgLAAYo7179z7zzDPOu5s2bXrxxReJ6A9/+MOmTZvG8ISNjY133303ET311FOuCgngtlDAADBGkZGRO3bscN597rnnjh8/rlAoTp069dxzz43hCd94443p06fPmjUrJSUlIiKira3NdWEB3A4OwgJgCYcUjRbeMfAOhYWFWAMGAABgAAUMAADAAI6CBmAM19cD8E0oYACWsDsTwGdhEzQAAAADKGAAAAAGUMAAAAAMoIABAAAYQAEDAAAwgAIGAABgAAUMAADAAAoYAACAARQwAAAAAzLCSHgAAACT7v8HdfxVje0div8AAAAASUVORK5CYII="/>
</div>
</article>
</section>
</body>
</html>




<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="SGPlot" data-sec-type="proc">
<h1 class="contentprocname toc">The SGPLOT Procedure</h1>
<article id="IDX">
<h1 class="contentitem toc">The SGPlot Procedure</h1>
<div class="c">
<img style="height: 480px; width: 640px" alt="The SGPlot Procedure" src="data:image/png;base64,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wp8sCG0MQQMAoAABDACAAgQwgOEZDIbnnntu0BZft+jT9wcCCgEMYESPPvpoTU2N6iqA0EQAAxjRI4888q1vfWvo9rq6uvXr11ut1vXr1zc0NOgbDQbD1q1b169frz/evHlzQkJCWlra22+//cMf/tDpdC5YsOD48eP6zuvXrzcYDGazOTMz84MPPvDbJwICB1dBA/5WWFJzqqRadRVfkJOemJ2eMHT7hg0bXnjhha1bt950000Dt99///1XXHHFhx9++Pjjj997772bN2/Wt3d2dn744Yf647KysoqKim3btl111VV//vOfH3nkkTfeeOPGG2/UM7h/t9dee23Tpk2FxopSjwAAAdVJREFUhYU+/HhAQDLk5+czNQLwg4KCAv3/tTd35L+1I7Am2Fy9dv6GtYP/HTAYDJqmNTQ0XHTRRR999FFsbKy+RURiYmJqa2vNZnNvb29iYmJjY6O+/6lTp7Kzs/tfO/B99Mdms9nlcg1qqH/jwD1lQI8BoaegoIAjYMDfctITDWsD62qjYQ9/dbGxsffee+93vvOdF198sX9jU1OT2WwWEavV2t7e/vf3yc4evSG3260/KCwsvP/++3fs2NHS0tK/EZhUCGDA37LTE0YJvAD05S9/+YUXXnjjjTf6t0RHR/f29lqt1t7eXofDMYH3vOaaazZt2vTUU085nU4ufsbkxEVYAM7tqaee+tGPftT/4y233PLoo4+KyM9+9rNbbrllAm9YXV19/fXXi8gPf/hDbxUJBBcCGMC5TZs27a677ur/8cEHH9yxY4fVat29e/eDDz44gTd84oknZs2aNXfu3JycnMTExKamJu8VCwQHLsIC/IRLisaLHkMIKygo4AgYAAAFCGAAABTgKmjAf1hfD0A/AhjwE05nAhiIIWgAABQggAEAUIAABgBAAQIYAAAFCGAAABQggAEAUIAABgBAAQIYAAAFCGAAABQwC7fHAwDA7/4/BF2wDohyeFIAAAAASUVORK5CYII="/>
</div>
</article>
</section>
</body>
</html>



#### Try out any other methods too. To see the method signature (parameters and return type) just type the method with a ? at the end and submit;<br><br>**<span style="color:blue; font-size:16;">cars.hist?</span>**<br><br>This will pop up a window at the bottome and show information about the method.


```python
#cars.hist?
```

### The SASsession object has a **submit** method to submit any SAS code you want.<br>It returns a dictionary with the LOG and the LST.<br>You can print the log and HTML the results from the Listing. <br> You can also prompt for macro variable substitution at runtime!


```python
 ll = sas.submit('data &dsname; user="&user"; hidden="&pw"; run; proc print data=&dsname;run;', prompt={'user': False, 'pw': True, 'dsname': False})
```

    Please enter value for macro variable user sastpw
    Please enter value for macro variable pw ········
    Please enter value for macro variable dsname tom1



```python
HTML(ll['LST'])
```




<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="Print" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<h1 class="contentprocname toc">The PRINT Procedure</h1>
<article>
<h1 class="contentitem toc">Data Set WORK.TOM1</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/></colgroup><colgroup><col/><col/></colgroup>
<thead>
<tr>
<th class="r header" scope="col">Obs</th>
<th class="header" scope="col">user</th>
<th class="header" scope="col">hidden</th>
</tr>
</thead>
<tbody>
<tr>
<th class="r rowheader" scope="row">1</th>
<td class="data">sastpw</td>
<td class="data">this is not my password</td>
</tr>
</tbody>
</table>
</article>
</section>
</body>
</html>





```python
print(ll['LOG'])
```

    
    60   ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;
    NOTE: Writing HTML5 Body file: STDOUT
    61   
    62   options nosource nonotes;
    67   data &dsname; user="&user"; hidden="&pw"; run; proc print data=&dsname;run;
    NOTE: The data set WORK.TOM1 has 1 observations and 2 variables.
    NOTE: DATA statement used (Total process time):
          real time           0.00 seconds
          cpu time            0.00 seconds
          
    NOTE: There were 1 observations read from the data set WORK.TOM1.
    NOTE: PROCEDURE PRINT used (Total process time):
          real time           0.00 seconds
          cpu time            0.01 seconds
          
    68   options nosource nonotes;
    73   
    74   ods html5 close;ods listing;
    
    75   


#### You can always see the entire session log by using the saslog() method of the SASsession object.


```python
#print(sas.saslog())
```


```python
ll = sas.submit('libname work list;')
```


```python
print(ll['LOG'])
```

    
    89   ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;
    NOTE: Writing HTML5 Body file: STDOUT
    90   
    91   libname work list;
    NOTE: Libref=   WORK 
          Scope=    Kernel  
          Engine=   V9
          Access=   TEMP
          Physical Name= /tmp/SAS_work7F250000113D_tom64-2
          Filename= /tmp/SAS_work7F250000113D_tom64-2
          Inode Number= 262147
          Access Permission= rwx------
          Owner Name= sas
          File Size=              4KB
          File Size (bytes)= 4096
    92   
    93   ods html5 close;ods listing;
    
    94   


## Want to read and write CSV files?


```python
cars.to_csv('/tmp/cars.csv')
```

    
    96   
    97   options nosource;
    NOTE: The file X is:
          Filename=/tmp/cars.csv,
          Owner Name=sas,Group Name=sas,
          Access Permission=-rw-rw-r--,
          Last Modified=15Jun2016:15:52:13
    
    NOTE: 429 records were written to the file X.
          The minimum record length was 68.
          The maximum record length was 123.
    NOTE: There were 428 observations read from the data set SASHELP.CARS.
    NOTE: DATA statement used (Total process time):
          real time           0.00 seconds
          cpu time            0.00 seconds
          
    428 records created in X from SASHELP.CARS.
      
      
    NOTE: "X" file was successfully created.
    NOTE: PROCEDURE EXPORT used (Total process time):
          real time           0.06 seconds
          cpu time            0.05 seconds
          
    184  
    185  
    186  



```python
carscsv = sas.read_csv('/tmp/cars.csv', 'cars_cvs')
```


```python
carscsv.tail(7)
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="Print" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<h1 class="contentprocname toc">The PRINT Procedure</h1>
<article>
<h1 class="contentitem toc">Data Set WORK.CARS_CVS</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/></colgroup><colgroup><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/></colgroup>
<thead>
<tr>
<th class="r header" scope="col">Obs</th>
<th class="header" scope="col">Make</th>
<th class="header" scope="col">Model</th>
<th class="header" scope="col">Type</th>
<th class="header" scope="col">Origin</th>
<th class="header" scope="col">DriveTrain</th>
<th class="header" scope="col">MSRP</th>
<th class="header" scope="col">Invoice</th>
<th class="r header" scope="col">EngineSize</th>
<th class="r header" scope="col">Cylinders</th>
<th class="r header" scope="col">Horsepower</th>
<th class="r header" scope="col">MPG_City</th>
<th class="r header" scope="col">MPG_Highway</th>
<th class="r header" scope="col">Weight</th>
<th class="r header" scope="col">Wheelbase</th>
<th class="r header" scope="col">Length</th>
</tr>
</thead>
<tbody>
<tr>
<th class="r rowheader" scope="row">422</th>
<td class="data">Volvo</td>
<td class="data">S80 2.9 4dr</td>
<td class="data">Sedan</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="data">$37,730</td>
<td class="data">$35,542</td>
<td class="r data">2.9</td>
<td class="r data">6</td>
<td class="r data">208</td>
<td class="r data">20</td>
<td class="r data">28</td>
<td class="r data">3576</td>
<td class="r data">110</td>
<td class="r data">190</td>
</tr>
<tr>
<th class="r rowheader" scope="row">423</th>
<td class="data">Volvo</td>
<td class="data">S80 2.5T 4dr</td>
<td class="data">Sedan</td>
<td class="data">Europe</td>
<td class="data">All</td>
<td class="data">$37,885</td>
<td class="data">$35,688</td>
<td class="r data">2.5</td>
<td class="r data">5</td>
<td class="r data">194</td>
<td class="r data">20</td>
<td class="r data">27</td>
<td class="r data">3691</td>
<td class="r data">110</td>
<td class="r data">190</td>
</tr>
<tr>
<th class="r rowheader" scope="row">424</th>
<td class="data">Volvo</td>
<td class="data">C70 LPT convertible 2dr</td>
<td class="data">Sedan</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="data">$40,565</td>
<td class="data">$38,203</td>
<td class="r data">2.4</td>
<td class="r data">5</td>
<td class="r data">197</td>
<td class="r data">21</td>
<td class="r data">28</td>
<td class="r data">3450</td>
<td class="r data">105</td>
<td class="r data">186</td>
</tr>
<tr>
<th class="r rowheader" scope="row">425</th>
<td class="data">Volvo</td>
<td class="data">C70 HPT convertible 2dr</td>
<td class="data">Sedan</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="data">$42,565</td>
<td class="data">$40,083</td>
<td class="r data">2.3</td>
<td class="r data">5</td>
<td class="r data">242</td>
<td class="r data">20</td>
<td class="r data">26</td>
<td class="r data">3450</td>
<td class="r data">105</td>
<td class="r data">186</td>
</tr>
<tr>
<th class="r rowheader" scope="row">426</th>
<td class="data">Volvo</td>
<td class="data">S80 T6 4dr</td>
<td class="data">Sedan</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="data">$45,210</td>
<td class="data">$42,573</td>
<td class="r data">2.9</td>
<td class="r data">6</td>
<td class="r data">268</td>
<td class="r data">19</td>
<td class="r data">26</td>
<td class="r data">3653</td>
<td class="r data">110</td>
<td class="r data">190</td>
</tr>
<tr>
<th class="r rowheader" scope="row">427</th>
<td class="data">Volvo</td>
<td class="data">V40</td>
<td class="data">Wagon</td>
<td class="data">Europe</td>
<td class="data">Front</td>
<td class="data">$26,135</td>
<td class="data">$24,641</td>
<td class="r data">1.9</td>
<td class="r data">4</td>
<td class="r data">170</td>
<td class="r data">22</td>
<td class="r data">29</td>
<td class="r data">2822</td>
<td class="r data">101</td>
<td class="r data">180</td>
</tr>
<tr>
<th class="r rowheader" scope="row">428</th>
<td class="data">Volvo</td>
<td class="data">XC70</td>
<td class="data">Wagon</td>
<td class="data">Europe</td>
<td class="data">All</td>
<td class="data">$35,145</td>
<td class="data">$33,112</td>
<td class="r data">2.5</td>
<td class="r data">5</td>
<td class="r data">208</td>
<td class="r data">20</td>
<td class="r data">27</td>
<td class="r data">3823</td>
<td class="r data">109</td>
<td class="r data">186</td>
</tr>
</tbody>
</table>
</article>
</section>
</body>
</html>




```python
 carscsv.means()
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="Means" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<div class="proc_title_group">
<p class="c proctitle">The MEANS Procedure</p>
</div>
<h1 class="contentprocname toc">The MEANS Procedure</h1>
<article>
<h1 class="contentitem toc">Summary statistics</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/></colgroup><colgroup><col/><col/><col/><col/><col/><col/><col/><col/></colgroup>
<thead>
<tr>
<th class="b header" scope="col">Variable</th>
<th class="r b header" scope="col">N</th>
<th class="r b header" scope="col">Mean</th>
<th class="r b header" scope="col">Std Dev</th>
<th class="r b header" scope="col">Minimum</th>
<th class="r b header" scope="col">25th Pctl</th>
<th class="r b header" scope="col">50th Pctl</th>
<th class="r b header" scope="col">75th Pctl</th>
<th class="r b header" scope="col">Maximum</th>
</tr>
</thead>
<tbody>
<tr>
<th class="data">
<div class="stacked-cell">
<div>EngineSize</div>
<div>Cylinders</div>
<div>Horsepower</div>
<div>MPG_City</div>
<div>MPG_Highway</div>
<div>Weight</div>
<div>Wheelbase</div>
<div>Length</div>
</div>
</th>
<td class="r data">
<div class="stacked-cell">
<div>428</div>
<div>426</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>3.1967290</div>
<div>5.8075117</div>
<div>215.8855140</div>
<div>20.0607477</div>
<div>26.8434579</div>
<div>3577.95</div>
<div>108.1542056</div>
<div>186.3621495</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>1.1085947</div>
<div>1.5584426</div>
<div>71.8360316</div>
<div>5.2382176</div>
<div>5.7412007</div>
<div>758.9832146</div>
<div>8.3118130</div>
<div>14.3579913</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>1.3000000</div>
<div>3.0000000</div>
<div>73.0000000</div>
<div>10.0000000</div>
<div>12.0000000</div>
<div>1850.00</div>
<div>89.0000000</div>
<div>143.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>2.3500000</div>
<div>4.0000000</div>
<div>165.0000000</div>
<div>17.0000000</div>
<div>24.0000000</div>
<div>3103.00</div>
<div>103.0000000</div>
<div>178.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>3.0000000</div>
<div>6.0000000</div>
<div>210.0000000</div>
<div>19.0000000</div>
<div>26.0000000</div>
<div>3474.50</div>
<div>107.0000000</div>
<div>187.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>3.9000000</div>
<div>6.0000000</div>
<div>255.0000000</div>
<div>21.5000000</div>
<div>29.0000000</div>
<div>3978.50</div>
<div>112.0000000</div>
<div>194.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>8.3000000</div>
<div>12.0000000</div>
<div>500.0000000</div>
<div>60.0000000</div>
<div>66.0000000</div>
<div>7190.00</div>
<div>144.0000000</div>
<div>238.0000000</div>
</div>
</td>
</tr>
</tbody>
</table>
</article>
</section>
</body>
</html>



## We can transfer data between SAS Data Sets and Pandas Data Frames 


```python
import pandas
```


```python
car_df = cars.to_df()
```


```python
car_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Make</th>
      <th>Model</th>
      <th>Type</th>
      <th>Origin</th>
      <th>DriveTrain</th>
      <th>MSRP</th>
      <th>Invoice</th>
      <th>EngineSize</th>
      <th>Cylinders</th>
      <th>Horsepower</th>
      <th>MPG_City</th>
      <th>MPG_Highway</th>
      <th>Weight</th>
      <th>Wheelbase</th>
      <th>Length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Acura</td>
      <td>MDX</td>
      <td>SUV</td>
      <td>Asia</td>
      <td>All</td>
      <td>36945</td>
      <td>33337</td>
      <td>3.5</td>
      <td>6.0</td>
      <td>265</td>
      <td>17</td>
      <td>23</td>
      <td>4451</td>
      <td>106</td>
      <td>189</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Acura</td>
      <td>RSX Type S 2dr</td>
      <td>Sedan</td>
      <td>Asia</td>
      <td>Front</td>
      <td>23820</td>
      <td>21761</td>
      <td>2.0</td>
      <td>4.0</td>
      <td>200</td>
      <td>24</td>
      <td>31</td>
      <td>2778</td>
      <td>101</td>
      <td>172</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Acura</td>
      <td>TSX 4dr</td>
      <td>Sedan</td>
      <td>Asia</td>
      <td>Front</td>
      <td>26990</td>
      <td>24647</td>
      <td>2.4</td>
      <td>4.0</td>
      <td>200</td>
      <td>22</td>
      <td>29</td>
      <td>3230</td>
      <td>105</td>
      <td>183</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Acura</td>
      <td>TL 4dr</td>
      <td>Sedan</td>
      <td>Asia</td>
      <td>Front</td>
      <td>33195</td>
      <td>30299</td>
      <td>3.2</td>
      <td>6.0</td>
      <td>270</td>
      <td>20</td>
      <td>28</td>
      <td>3575</td>
      <td>108</td>
      <td>186</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Acura</td>
      <td>3.5 RL 4dr</td>
      <td>Sedan</td>
      <td>Asia</td>
      <td>Front</td>
      <td>43755</td>
      <td>39014</td>
      <td>3.5</td>
      <td>6.0</td>
      <td>225</td>
      <td>18</td>
      <td>24</td>
      <td>3880</td>
      <td>115</td>
      <td>197</td>
    </tr>
  </tbody>
</table>
</div>




```python
cars.head()
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="Print" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<h1 class="contentprocname toc">The PRINT Procedure</h1>
<article>
<h1 class="contentitem toc">Data Set SASHELP.CARS</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/></colgroup><colgroup><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/></colgroup>
<thead>
<tr>
<th class="r header" scope="col">Obs</th>
<th class="header" scope="col">Make</th>
<th class="header" scope="col">Model</th>
<th class="header" scope="col">Type</th>
<th class="header" scope="col">Origin</th>
<th class="header" scope="col">DriveTrain</th>
<th class="r header" scope="col">MSRP</th>
<th class="r header" scope="col">Invoice</th>
<th class="r header" scope="col">EngineSize</th>
<th class="r header" scope="col">Cylinders</th>
<th class="r header" scope="col">Horsepower</th>
<th class="r header" scope="col">MPG_City</th>
<th class="r header" scope="col">MPG_Highway</th>
<th class="r header" scope="col">Weight</th>
<th class="r header" scope="col">Wheelbase</th>
<th class="r header" scope="col">Length</th>
</tr>
</thead>
<tbody>
<tr>
<th class="r rowheader" scope="row">1</th>
<td class="data">Acura</td>
<td class="data">MDX</td>
<td class="data">SUV</td>
<td class="data">Asia</td>
<td class="data">All</td>
<td class="r data">$36,945</td>
<td class="r data">$33,337</td>
<td class="r data">3.5</td>
<td class="r data">6</td>
<td class="r data">265</td>
<td class="r data">17</td>
<td class="r data">23</td>
<td class="r data">4451</td>
<td class="r data">106</td>
<td class="r data">189</td>
</tr>
<tr>
<th class="r rowheader" scope="row">2</th>
<td class="data">Acura</td>
<td class="data">RSX Type S 2dr</td>
<td class="data">Sedan</td>
<td class="data">Asia</td>
<td class="data">Front</td>
<td class="r data">$23,820</td>
<td class="r data">$21,761</td>
<td class="r data">2.0</td>
<td class="r data">4</td>
<td class="r data">200</td>
<td class="r data">24</td>
<td class="r data">31</td>
<td class="r data">2778</td>
<td class="r data">101</td>
<td class="r data">172</td>
</tr>
<tr>
<th class="r rowheader" scope="row">3</th>
<td class="data">Acura</td>
<td class="data">TSX 4dr</td>
<td class="data">Sedan</td>
<td class="data">Asia</td>
<td class="data">Front</td>
<td class="r data">$26,990</td>
<td class="r data">$24,647</td>
<td class="r data">2.4</td>
<td class="r data">4</td>
<td class="r data">200</td>
<td class="r data">22</td>
<td class="r data">29</td>
<td class="r data">3230</td>
<td class="r data">105</td>
<td class="r data">183</td>
</tr>
<tr>
<th class="r rowheader" scope="row">4</th>
<td class="data">Acura</td>
<td class="data">TL 4dr</td>
<td class="data">Sedan</td>
<td class="data">Asia</td>
<td class="data">Front</td>
<td class="r data">$33,195</td>
<td class="r data">$30,299</td>
<td class="r data">3.2</td>
<td class="r data">6</td>
<td class="r data">270</td>
<td class="r data">20</td>
<td class="r data">28</td>
<td class="r data">3575</td>
<td class="r data">108</td>
<td class="r data">186</td>
</tr>
<tr>
<th class="r rowheader" scope="row">5</th>
<td class="data">Acura</td>
<td class="data">3.5 RL 4dr</td>
<td class="data">Sedan</td>
<td class="data">Asia</td>
<td class="data">Front</td>
<td class="r data">$43,755</td>
<td class="r data">$39,014</td>
<td class="r data">3.5</td>
<td class="r data">6</td>
<td class="r data">225</td>
<td class="r data">18</td>
<td class="r data">24</td>
<td class="r data">3880</td>
<td class="r data">115</td>
<td class="r data">197</td>
</tr>
</tbody>
</table>
</article>
</section>
</body>
</html>




```python
car_df.dtypes
```




    Make            object
    Model           object
    Type            object
    Origin          object
    DriveTrain      object
    MSRP             int64
    Invoice          int64
    EngineSize     float64
    Cylinders      float64
    Horsepower       int64
    MPG_City         int64
    MPG_Highway      int64
    Weight           int64
    Wheelbase        int64
    Length           int64
    dtype: object




```python
cars.contents()
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="Contents" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<div class="proc_title_group">
<p class="c proctitle">The CONTENTS Procedure</p>
</div>
<h1 class="contentprocname toc">The CONTENTS Procedure</h1>
<section>
<h1 class="contentfolder toc">SASHELP.CARS</h1>
<article>
<h1 class="contentitem toc">Attributes</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/><col/><col/><col/></colgroup>
<tbody>
<tr>
<th class="rowheader" scope="row">Data Set Name</th>
<td class="data">SASHELP.CARS</td>
<th class="rowheader" scope="row">Observations</th>
<td class="data">428</td>
</tr>
<tr>
<th class="rowheader" scope="row">Member Type</th>
<td class="data">DATA</td>
<th class="rowheader" scope="row">Variables</th>
<td class="data">15</td>
</tr>
<tr>
<th class="rowheader" scope="row">Engine</th>
<td class="data">V9</td>
<th class="rowheader" scope="row">Indexes</th>
<td class="data">0</td>
</tr>
<tr>
<th class="rowheader" scope="row">Created</th>
<td class="data">05/27/2015 21:17:15</td>
<th class="rowheader" scope="row">Observation Length</th>
<td class="data">152</td>
</tr>
<tr>
<th class="rowheader" scope="row">Last Modified</th>
<td class="data">05/27/2015 21:17:15</td>
<th class="rowheader" scope="row">Deleted Observations</th>
<td class="data">0</td>
</tr>
<tr>
<th class="rowheader" scope="row">Protection</th>
<td class="data">&#160;</td>
<th class="rowheader" scope="row">Compressed</th>
<td class="data">NO</td>
</tr>
<tr>
<th class="rowheader" scope="row">Data Set Type</th>
<td class="data">&#160;</td>
<th class="rowheader" scope="row">Sorted</th>
<td class="data">YES</td>
</tr>
<tr>
<th class="rowheader" scope="row">Label</th>
<td class="data">2004 Car Data</td>
<th class="rowheader" scope="row">&#160;</th>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="rowheader" scope="row">Data Representation</th>
<td class="data">SOLARIS_X86_64, LINUX_X86_64, ALPHA_TRU64, LINUX_IA64</td>
<th class="rowheader" scope="row">&#160;</th>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="rowheader" scope="row">Encoding</th>
<td class="data">us-ascii  ASCII (ANSI)</td>
<th class="rowheader" scope="row">&#160;</th>
<td class="data">&#160;</td>
</tr>
</tbody>
</table>
</article>
<article id="IDX1">
<h1 class="contentitem toc">Engine/Host Information</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/><col/></colgroup>
<thead>
<tr>
<th class="c b header" colspan="2" scope="colgroup">Engine/Host Dependent Information</th>
</tr>
</thead>
<tbody>
<tr>
<th class="rowheader" scope="row">Data Set Page Size</th>
<td class="data">65536</td>
</tr>
<tr>
<th class="rowheader" scope="row">Number of Data Set Pages</th>
<td class="data">2</td>
</tr>
<tr>
<th class="rowheader" scope="row">First Data Page</th>
<td class="data">1</td>
</tr>
<tr>
<th class="rowheader" scope="row">Max Obs per Page</th>
<td class="data">430</td>
</tr>
<tr>
<th class="rowheader" scope="row">Obs in First Data Page</th>
<td class="data">405</td>
</tr>
<tr>
<th class="rowheader" scope="row">Number of Data Set Repairs</th>
<td class="data">0</td>
</tr>
<tr>
<th class="rowheader" scope="row">Filename</th>
<td class="data">/opt/tom/sasutf8/SASFoundation/9.4/sashelp/cars.sas7bdat</td>
</tr>
<tr>
<th class="rowheader" scope="row">Release Created</th>
<td class="data">9.0401M3</td>
</tr>
<tr>
<th class="rowheader" scope="row">Host Created</th>
<td class="data">Linux</td>
</tr>
<tr>
<th class="rowheader" scope="row">Inode Number</th>
<td class="data">7209257</td>
</tr>
<tr>
<th class="rowheader" scope="row">Access Permission</th>
<td class="data">rw-r--r--</td>
</tr>
<tr>
<th class="rowheader" scope="row">Owner Name</th>
<td class="data">sastpw</td>
</tr>
<tr>
<th class="rowheader" scope="row">File Size</th>
<td class="data">192KB</td>
</tr>
<tr>
<th class="rowheader" scope="row">File Size (bytes)</th>
<td class="data">196608</td>
</tr>
</tbody>
</table>
</article>
<article id="IDX2">
<h1 class="contentitem toc">Variables</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/></colgroup><colgroup><col/><col/><col/><col/><col/></colgroup>
<thead>
<tr>
<th class="c b header" colspan="6" scope="colgroup">Alphabetic List of Variables and Attributes</th>
</tr>
<tr>
<th class="r b header" scope="col">#</th>
<th class="b header" scope="col">Variable</th>
<th class="b header" scope="col">Type</th>
<th class="r b header" scope="col">Len</th>
<th class="b header" scope="col">Format</th>
<th class="b header" scope="col">Label</th>
</tr>
</thead>
<tbody>
<tr>
<th class="r rowheader" scope="row">9</th>
<td class="data">Cylinders</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">5</th>
<td class="data">DriveTrain</td>
<td class="data">Char</td>
<td class="r data">5</td>
<td class="data">&#160;</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">8</th>
<td class="data">EngineSize</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">Engine Size (L)</td>
</tr>
<tr>
<th class="r rowheader" scope="row">10</th>
<td class="data">Horsepower</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">7</th>
<td class="data">Invoice</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">DOLLAR8.</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">15</th>
<td class="data">Length</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">Length (IN)</td>
</tr>
<tr>
<th class="r rowheader" scope="row">11</th>
<td class="data">MPG_City</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">MPG (City)</td>
</tr>
<tr>
<th class="r rowheader" scope="row">12</th>
<td class="data">MPG_Highway</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">MPG (Highway)</td>
</tr>
<tr>
<th class="r rowheader" scope="row">6</th>
<td class="data">MSRP</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">DOLLAR8.</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">1</th>
<td class="data">Make</td>
<td class="data">Char</td>
<td class="r data">13</td>
<td class="data">&#160;</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">2</th>
<td class="data">Model</td>
<td class="data">Char</td>
<td class="r data">40</td>
<td class="data">&#160;</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">4</th>
<td class="data">Origin</td>
<td class="data">Char</td>
<td class="r data">6</td>
<td class="data">&#160;</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">3</th>
<td class="data">Type</td>
<td class="data">Char</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">&#160;</td>
</tr>
<tr>
<th class="r rowheader" scope="row">13</th>
<td class="data">Weight</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">Weight (LBS)</td>
</tr>
<tr>
<th class="r rowheader" scope="row">14</th>
<td class="data">Wheelbase</td>
<td class="data">Num</td>
<td class="r data">8</td>
<td class="data">&#160;</td>
<td class="data">Wheelbase (IN)</td>
</tr>
</tbody>
</table>
</article>
<article id="IDX3">
<h1 class="contentitem toc">Sortedby</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/><col/></colgroup>
<thead>
<tr>
<th class="c b header" colspan="2" scope="colgroup">Sort Information</th>
</tr>
</thead>
<tbody>
<tr>
<th class="rowheader" scope="row">Sortedby</th>
<td class="data">Make Type</td>
</tr>
<tr>
<th class="rowheader" scope="row">Validated</th>
<td class="data">YES</td>
</tr>
<tr>
<th class="rowheader" scope="row">Character Set</th>
<td class="data">ANSI</td>
</tr>
</tbody>
</table>
</article>
</section>
</section>
</body>
</html>



 Data Frames **describe** method matches up with our Proc Means. SASdata object has the **describe** method (and **means** as an alias method)


```python
car_df.describe()
```

    /usr/lib64/python3.5/site-packages/numpy/lib/function_base.py:3823: RuntimeWarning: Invalid value encountered in percentile
      RuntimeWarning)





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MSRP</th>
      <th>Invoice</th>
      <th>EngineSize</th>
      <th>Cylinders</th>
      <th>Horsepower</th>
      <th>MPG_City</th>
      <th>MPG_Highway</th>
      <th>Weight</th>
      <th>Wheelbase</th>
      <th>Length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>428.000000</td>
      <td>428.000000</td>
      <td>428.000000</td>
      <td>426.000000</td>
      <td>428.000000</td>
      <td>428.000000</td>
      <td>428.000000</td>
      <td>428.000000</td>
      <td>428.000000</td>
      <td>428.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>32774.855140</td>
      <td>30014.700935</td>
      <td>3.196729</td>
      <td>5.807512</td>
      <td>215.885514</td>
      <td>20.060748</td>
      <td>26.843458</td>
      <td>3577.953271</td>
      <td>108.154206</td>
      <td>186.362150</td>
    </tr>
    <tr>
      <th>std</th>
      <td>19431.716674</td>
      <td>17642.117750</td>
      <td>1.108595</td>
      <td>1.558443</td>
      <td>71.836032</td>
      <td>5.238218</td>
      <td>5.741201</td>
      <td>758.983215</td>
      <td>8.311813</td>
      <td>14.357991</td>
    </tr>
    <tr>
      <th>min</th>
      <td>10280.000000</td>
      <td>9875.000000</td>
      <td>1.300000</td>
      <td>3.000000</td>
      <td>73.000000</td>
      <td>10.000000</td>
      <td>12.000000</td>
      <td>1850.000000</td>
      <td>89.000000</td>
      <td>143.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>20334.250000</td>
      <td>18866.000000</td>
      <td>2.375000</td>
      <td>NaN</td>
      <td>165.000000</td>
      <td>17.000000</td>
      <td>24.000000</td>
      <td>3104.000000</td>
      <td>103.000000</td>
      <td>178.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>27635.000000</td>
      <td>25294.500000</td>
      <td>3.000000</td>
      <td>NaN</td>
      <td>210.000000</td>
      <td>19.000000</td>
      <td>26.000000</td>
      <td>3474.500000</td>
      <td>107.000000</td>
      <td>187.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>39205.000000</td>
      <td>35710.250000</td>
      <td>3.900000</td>
      <td>NaN</td>
      <td>255.000000</td>
      <td>21.250000</td>
      <td>29.000000</td>
      <td>3977.750000</td>
      <td>112.000000</td>
      <td>194.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>192465.000000</td>
      <td>173560.000000</td>
      <td>8.300000</td>
      <td>12.000000</td>
      <td>500.000000</td>
      <td>60.000000</td>
      <td>66.000000</td>
      <td>7190.000000</td>
      <td>144.000000</td>
      <td>238.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
cars.describe()
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="Means" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<div class="proc_title_group">
<p class="c proctitle">The MEANS Procedure</p>
</div>
<h1 class="contentprocname toc">The MEANS Procedure</h1>
<article>
<h1 class="contentitem toc">Summary statistics</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/><col/></colgroup><colgroup><col/><col/><col/><col/><col/><col/><col/><col/></colgroup>
<thead>
<tr>
<th class="b header" scope="col">Variable</th>
<th class="b header" scope="col">Label</th>
<th class="r b header" scope="col">N</th>
<th class="r b header" scope="col">Mean</th>
<th class="r b header" scope="col">Std Dev</th>
<th class="r b header" scope="col">Minimum</th>
<th class="r b header" scope="col">25th Pctl</th>
<th class="r b header" scope="col">50th Pctl</th>
<th class="r b header" scope="col">75th Pctl</th>
<th class="r b header" scope="col">Maximum</th>
</tr>
</thead>
<tbody>
<tr>
<th class="data">
<div class="stacked-cell">
<div>MSRP</div>
<div>Invoice</div>
<div>EngineSize</div>
<div>Cylinders</div>
<div>Horsepower</div>
<div>MPG_City</div>
<div>MPG_Highway</div>
<div>Weight</div>
<div>Wheelbase</div>
<div>Length</div>
</div>
</th>
<th class="data">
<div class="stacked-cell">
<div>&#160;</div>
<div>&#160;</div>
<div>Engine Size (L)</div>
<div>&#160;</div>
<div>&#160;</div>
<div>MPG (City)</div>
<div>MPG (Highway)</div>
<div>Weight (LBS)</div>
<div>Wheelbase (IN)</div>
<div>Length (IN)</div>
</div>
</th>
<td class="r data">
<div class="stacked-cell">
<div>428</div>
<div>428</div>
<div>428</div>
<div>426</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>32774.86</div>
<div>30014.70</div>
<div>3.1967290</div>
<div>5.8075117</div>
<div>215.8855140</div>
<div>20.0607477</div>
<div>26.8434579</div>
<div>3577.95</div>
<div>108.1542056</div>
<div>186.3621495</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>19431.72</div>
<div>17642.12</div>
<div>1.1085947</div>
<div>1.5584426</div>
<div>71.8360316</div>
<div>5.2382176</div>
<div>5.7412007</div>
<div>758.9832146</div>
<div>8.3118130</div>
<div>14.3579913</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>10280.00</div>
<div>9875.00</div>
<div>1.3000000</div>
<div>3.0000000</div>
<div>73.0000000</div>
<div>10.0000000</div>
<div>12.0000000</div>
<div>1850.00</div>
<div>89.0000000</div>
<div>143.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>20329.50</div>
<div>18851.00</div>
<div>2.3500000</div>
<div>4.0000000</div>
<div>165.0000000</div>
<div>17.0000000</div>
<div>24.0000000</div>
<div>3103.00</div>
<div>103.0000000</div>
<div>178.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>27635.00</div>
<div>25294.50</div>
<div>3.0000000</div>
<div>6.0000000</div>
<div>210.0000000</div>
<div>19.0000000</div>
<div>26.0000000</div>
<div>3474.50</div>
<div>107.0000000</div>
<div>187.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>39215.00</div>
<div>35732.50</div>
<div>3.9000000</div>
<div>6.0000000</div>
<div>255.0000000</div>
<div>21.5000000</div>
<div>29.0000000</div>
<div>3978.50</div>
<div>112.0000000</div>
<div>194.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>192465.00</div>
<div>173560.00</div>
<div>8.3000000</div>
<div>12.0000000</div>
<div>500.0000000</div>
<div>60.0000000</div>
<div>66.0000000</div>
<div>7190.00</div>
<div>144.0000000</div>
<div>238.0000000</div>
</div>
</td>
</tr>
</tbody>
</table>
</article>
</section>
</body>
</html>



## Now round trip the Data Frame back to a SAS Data Set


```python
cars_full_circle = sas.df2sd(car_df, 'cfc')
```


```python
cars_full_circle.describe()
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="Means" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<div class="proc_title_group">
<p class="c proctitle">The MEANS Procedure</p>
</div>
<h1 class="contentprocname toc">The MEANS Procedure</h1>
<article>
<h1 class="contentitem toc">Summary statistics</h1>
<table class="table" style="border-spacing: 0">
<colgroup><col/></colgroup><colgroup><col/><col/><col/><col/><col/><col/><col/><col/></colgroup>
<thead>
<tr>
<th class="b header" scope="col">Variable</th>
<th class="r b header" scope="col">N</th>
<th class="r b header" scope="col">Mean</th>
<th class="r b header" scope="col">Std Dev</th>
<th class="r b header" scope="col">Minimum</th>
<th class="r b header" scope="col">25th Pctl</th>
<th class="r b header" scope="col">50th Pctl</th>
<th class="r b header" scope="col">75th Pctl</th>
<th class="r b header" scope="col">Maximum</th>
</tr>
</thead>
<tbody>
<tr>
<th class="data">
<div class="stacked-cell">
<div>MSRP</div>
<div>Invoice</div>
<div>EngineSize</div>
<div>Cylinders</div>
<div>Horsepower</div>
<div>MPG_City</div>
<div>MPG_Highway</div>
<div>Weight</div>
<div>Wheelbase</div>
<div>Length</div>
</div>
</th>
<td class="r data">
<div class="stacked-cell">
<div>428</div>
<div>428</div>
<div>428</div>
<div>426</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
<div>428</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>32774.86</div>
<div>30014.70</div>
<div>3.1967290</div>
<div>5.8075117</div>
<div>215.8855140</div>
<div>20.0607477</div>
<div>26.8434579</div>
<div>3577.95</div>
<div>108.1542056</div>
<div>186.3621495</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>19431.72</div>
<div>17642.12</div>
<div>1.1085947</div>
<div>1.5584426</div>
<div>71.8360316</div>
<div>5.2382176</div>
<div>5.7412007</div>
<div>758.9832146</div>
<div>8.3118130</div>
<div>14.3579913</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>10280.00</div>
<div>9875.00</div>
<div>1.3000000</div>
<div>3.0000000</div>
<div>73.0000000</div>
<div>10.0000000</div>
<div>12.0000000</div>
<div>1850.00</div>
<div>89.0000000</div>
<div>143.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>20329.50</div>
<div>18851.00</div>
<div>2.3500000</div>
<div>4.0000000</div>
<div>165.0000000</div>
<div>17.0000000</div>
<div>24.0000000</div>
<div>3103.00</div>
<div>103.0000000</div>
<div>178.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>27635.00</div>
<div>25294.50</div>
<div>3.0000000</div>
<div>6.0000000</div>
<div>210.0000000</div>
<div>19.0000000</div>
<div>26.0000000</div>
<div>3474.50</div>
<div>107.0000000</div>
<div>187.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>39215.00</div>
<div>35732.50</div>
<div>3.9000000</div>
<div>6.0000000</div>
<div>255.0000000</div>
<div>21.5000000</div>
<div>29.0000000</div>
<div>3978.50</div>
<div>112.0000000</div>
<div>194.0000000</div>
</div>
</td>
<td class="r data">
<div class="stacked-cell">
<div>192465.00</div>
<div>173560.00</div>
<div>8.3000000</div>
<div>12.0000000</div>
<div>500.0000000</div>
<div>60.0000000</div>
<div>66.0000000</div>
<div>7190.00</div>
<div>144.0000000</div>
<div>238.0000000</div>
</div>
</td>
</tr>
</tbody>
</table>
</article>
</section>
</body>
</html>



# Now let's look at the SASstat object!


```python
stat = sas.sasstat()
```


```python
#stat.                 # use the 'dot Tab ' to see the methods available
```

### Let's run a regression which will return us a SASresults object that we can use to see any/all of the results


```python
stat_results = stat.reg(model='horsepower = Cylinders EngineSize', data=cars)
```

### What results are available?


```python
dir(stat_results)
```




    ['ANOVA',
     'COOKSDPLOT',
     'DFBETASPANEL',
     'DFFITSPLOT',
     'DIAGNOSTICSPANEL',
     'FITSTATISTICS',
     'NOBS',
     'OBSERVEDBYPREDICTED',
     'PARAMETERESTIMATES',
     'QQPLOT',
     'RESIDUALBOXPLOT',
     'RESIDUALBYPREDICTED',
     'RESIDUALHISTOGRAM',
     'RESIDUALPLOT',
     'RFPLOT',
     'RSTUDENTBYLEVERAGE',
     'RSTUDENTBYPREDICTED']



### Pick any one you want ...


```python
stat_results.DIAGNOSTICSPANEL
```




<h1>DIAGNOSTICSPANEL</h1><!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="DOCUMENT" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<div class="proc_title_group">
<p class="c proctitle">The REG Procedure</p>
<p class="c proctitle">Model: MODEL1</p>
<p class="c proctitle">Dependent Variable: Horsepower</p>
</div>
<h1 class="contentproclabel toc">The Reg Procedure</h1>
<section>
<h1 class="contentfolder toc">MODEL1</h1>
<section>
<h1 class="contentfolder toc">Observation-wise Statistics</h1>
<section>
<h1 class="contentfolder toc">Horsepower</h1>
<section>
<h1 class="contentfolder toc">Diagnostic Plots</h1>
<article>
<h1 class="contentitem toc">Fit Diagnostics</h1>
<div class="c">
<img style="height: 640px; width: 640px" alt="Fit Diagnostics" src="data:image/png;base64,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"/>
</div>
</article>
</section>
</section>
</section>
</section>
</section>
</body>
</html>




### Or display them ALL  (Click in the pannel to the Left of the results below to expand/shrink the result pane)


```python
#stat_results.ALL()
```

### Proc SQL anyone???  
#### And you can use the SASLIB method of the SASsession to assign any data you like (Teradata, Hadoop, ...)


```python
#sas.saslib('Tera', engine='Teradata', options='user=me pw=mypw server=teracop1')
ll = sas.submit('proc sql; create table sales as select month, sum(actual) as tot_sales, sum(predict) as predicted_sales from sashelp.prdsale group by 1 order by month ;quit;')
sales = sas.sasdata('sales')
```


```python
print(ll['LOG']);HTML(ll['LST'])
```

    
    1078  ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;
    NOTE: Writing HTML5 Body file: STDOUT
    1079  
    1080  proc sql;
    1080!           create table sales as select month, sum(actual) as tot_sales, sum(predict) as predicted_sales from sashelp.prdsale
    1080! group by 1 order by month ;quit;
    NOTE: Table WORK.SALES created, with 24 rows and 3 columns.
    
    NOTE: PROCEDURE SQL used (Total process time):
          real time           0.00 seconds
          cpu time            0.02 seconds
          
    1081  
    1082  ods html5 close;ods listing;
    
    1083  









### Let's chart our sales for the aggregate table we created with the Proc SQL


```python
sales.series(y=['tot_sales','predicted_sales'], x='month', title='total vs. predicted sales')
```


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="SGPlot" data-sec-type="proc">
<h1 class="contentprocname toc">The SGPLOT Procedure</h1>
<article id="IDX">
<h1 class="contentitem toc">The SGPlot Procedure</h1>
<div class="c">
<img style="height: 480px; width: 640px" alt="The SGPlot Procedure" src="data:image/png;base64,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"/>
</div>
</article>
</section>
</body>
</html>



## Try the ETS object; including cheking an error case first


```python
ets = sas.sasets()
```


```python
ets_results = ets.arima(model='horsepower = Cylinders EngineSize', data=cars)
```

    You are missing 1 required statements:
    {'identify'}
    Error in code submission



```python
dir(ets_results)
```




    []




```python
ets_results.PLOT
```

    Result named PLOT not found. Valid results are:[]



```python
ets_results = ets.timeid(id='horsepower', data=cars)
```


```python
dir(ets_results)
```




    ['DECOMPOSITIONPLOT',
     'INTERVALCOUNTSCOMPONENTPLOT',
     'OFFSETCOMPONENTPLOT',
     'SPANCOMPONENTPLOT',
     'VALUESPLOT']




```python
ets_results.DECOMPOSITIONPLOT
```




<h1>DECOMPOSITIONPLOT</h1><!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="DOCUMENT" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<div class="proc_title_group">
<p class="c proctitle">The TIMEID Procedure</p>
</div>
<h1 class="contentproclabel toc">The Timeid Procedure</h1>
<section>
<h1 class="contentfolder toc">Decomposition</h1>
<article>
<h1 class="contentitem toc">Time ID Decomposition Plot for WEEKDAY145W BEGIN</h1>
<div class="c">
<img style="height: 480px; width: 640px" alt="Time ID Decomposition Plot for WEEKDAY145W BEGIN" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAIAAAC6s0uzAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAgAElEQVR4nOzde1xUdf4/8PcMM8MMzAAid8Ub4v2Gl6xMYd0iqyXT7LIZueWWtVvtt5+r7bYZWZa5ttVutuVWXvJOaQJeUvGKKd64328idxjuDDD3+f1x9HAccIBhmAP4ej74Y845n3POa86cmTfnLkhOTiYAAACwLxERTZkyhe8YAAAAd5GUlBQh3xkAAADuRijAAAAAPEABBgAA4AEKMAAAAA9QgAEAAHiAAgwAAMADFGAAAAAeoAADAADwAAUYAACAByjAAAAAPEABBgAA4AEKMAAAAA9QgAcOgUVENGfOnDlz5vTSfNtnkEqlc+fO3bNnT1cCd9q4P7KwwG37WcTFxU2YMEEkEgUEBFg9EV9fX4FAUF5eTkRGo1EkEgkEApFIZDQaiUipVAoEAk9PT7rzmsZMpytDufM9fvy4XC4XCATffPMNdXmtCAgIEAgETk5OWq2WiNRq9ciRIwUCwdmzZ7nNTp8+LRAIRo4cqVar2WXVPgMRJSUlmfXvMH/XlxKX2aQkEsm4ceMiIiLYVJYXGuPKlStLly51c3OTSCQuLi5PPPFEdHS02Sy4r4ODg9tnaL8kgU/JyckmGBAsf9Amk+n++++///77e2m+FjKsXLmy64Hv1Lg/4i5w7lIy2fqzGDVqFDP9F154weqJPPnkk0QUFRVlMpni4+PZT+T8+fMmkykmJoaIFi1aZLrzmsZMpytD2ZlGRUU5OjrKZLKYmBgLo5utFadOnWIHbdmyhel57NgxIgoMDNRoNEwfjUbDLJljx46ZTCaDwRAZGenl5WWWgREUFGTWv8P8XV9KXHdaJs8++2xXFprJZPrggw86bPDwww+3X7DsUHaptl/ywLvk5GQU4IHJnl+29t985nVTU9Mnn3zC9Dlx4oTlETtt3N/16ifi4OBARA0NDT2ZCPMTv3HjRpPJtHPnTiIaNGgQEf3www8mk+nzzz8norffftvU2Xvp+tC9e/c6ODh4eXnFx8d32OBOa8Xzzz9PREzJDAkJYfs/99xzRPTOO+8wne+88w4RPf/889wpjxgxon3CzZs3t695Hb6Rri8lC8vEYDAcPXqUiGQyWVcW2t69e4lILBZv3LiR+ZTLysq2bdv2wAMP/Pzzz+2nwL6X8ePHGwyGrswC7A8FeMDq8MvW/iu6e/fusWPHurq6/vDDD6tWrXJ2dvbx8eH+0qWmpoaFhclksvnz5ycmJnY6r/bzXbduHREtXLiwKyHbN7YQID4+/uGHH5bJZI6OjvPmzWP/2d+yZUtgYKBYLA4MDGQ3j7r4lpk2+/fvHzp06KhRo7ijW5hyfn7+gw8+yCSZP38+s73FfYN0u/bv3XLm7777btSoUWKx+J577snPz+9wMXZrgunp6cOGDRs1ahR3Oj///DMRPffccyaT6ZVXXmFeE9FLL71kulXb9u/f3+EH1z5Pp0O/++47Iho1alRhYaHl0c3WitraWrFYLBaLc3NzxWIxEbHLpLq62sPDw8HBITU1NTk52cHBwcPDo7q6mhnq6Oi4aNGiwsJCs1nU1tZ6eHhMnjzZrH+Hb6TrS8nCmzIYDFFRUUQUFBTUlYXG/KthtjZamAXz+qmnniKizz//vCuzAPtDAR6wOvyytf+Kdmjq1KlMmwsXLjg6OrL9ZTJZh2tL+8lyh1ZXVxORQqHoSkizxhYCxMfHMz++rAceeMBkMkVGRpq9HfbXsCtvmelkNigZ27ZtYwZZmPL48eO5/dnCxr5BsxHN3nu3MjNvs/1i7NYEH3jgAWq3v5pZ+MyiePDBB4no8OHDdGsTc8aMGUSUm5t7pyXZYZ47Df3Xv/5FRBMnTqyqquruWsFsZTI7b5mC995777GNma3SqVOnMkWL2TC1PIs33niDiNiFZtZMJpM98MADZ86c6e5SutNnxAoJCWH/+bC80BwcHMRiMbst2yHuKMzr/Px8sVg8aNAgZqO5/YIFfqEAD1gdftnaf0U3b95cUlLCvmY2DsRiMdNm3rx5dOtwF/Mr0+mGbIfzZX4+uhiS29hCgPnz5xPRH//4R41GU1RU9PDDDzPN7r33XiL65JNPTLf2Ft5zzz1df8tsf9OtDS+2NluYMvNfwubNm1tbWyMjI9kDlhaWDLez08xvvPGGRqNhDnx2ZUl2OsGJEydWVFS0n86gQYOYH3rmuCzz1hwdHQ0Gg1gsdnR05E7kTtWii0MdHBwcHBxOnTpl+b0wuGsFs6nK7LRglsnQoUO5jZm6SETz589v/x7NZpGamkpEkydPbj/riRMncv8VY3eTdHEptZ+jGR8fnwsXLnRxoZl97u2bdfh61apVRLRq1ao7LVjgEQrwgNXhl63Tr6vZa+7WJ6PTDdn282V+lbq4BWzW2EIAZhB7uo1Op2NeMJvFzLaCTqejOxxm68prg8HA/eGzMOV///vfzIh+fn47d+7sypLhdnYxc4dLrMP+nU7w3Llz7SdiMpkWLVpEtzbpmOrF/A/EnFvEHm21/FPelaGrVq2Kj49XKBSDBg1KT0+3PDp3reCe98TFPW6Sn5/P9Gy/u779LJidAZGRkXdKbjAYvvzySyKaN29et5aShTel0WiYY9sTJ07sykJTKBTWFeCGhgYPDw+xWMwukzvNAuwvOTkZlyFBN7S0tHR3lK1bt+p0uscee8wmja0IYDXmwhKRSNRpyzfffDM1NfUPf/hDZWXl888//7e//a330/XI3LlzO+zPbFzu2rWLiEaPHk1EzFnETB/2XOue++c//zl79uyoqCiVSvXII48olUoLjblrBXPkuMM27Gs2Z1cCnz9/noiefvpp7jU83AZCofD1118nokuXLjF9er6UJBIJs22ak5PTaWMiCg0N1el0Bw4cYPswv+Cdjuji4vL3v/9dp9P1/XXyLoUt4AGJ+XAt9OzKa2Y375dffsluX3Y6L+7r2tra999/n9mJd/XqVcsjdtjYQgBm0CuvvMLsgn7ssce4u6DXrVtnMpnee+89Irr33nu7+/aZA4fvv/8+cY65WpjyO++8w5x4deHCBbK4zV1WVtZ+UBczt++8U/+uT9AMc4aRh4cHEe3evdtkMv3www9sH3bj3vJEujWUORfpnnvuaW1tbd/AbK1obW2VyWQODg7c/edlZWXMDmruSeBdz0AdMZlMq1at2rlzp06nMxgMzJowduzYbi0lC++6ubn53XffpS5vATPb/Y6Ojh9//DHz3jUaDXMedaertMFgGDt2LPetQR+BXdADVodftq58Xbmvz58/b3aiU6e71zr8OWMORt5pRAuNLQRoP6iLJ2F15TUXU9ctTzkwMJDbn/2l5k6ZPVGLOfWJO6iLme/0sbbv3/UJmikrK2NHuXz5MrOc2T7Mpa53+uDI4jpAHS1tBnPaVFhYmIXRmbWCuViIbckKCwsjoq+++qrTBdX1xejn52eWYe/evd1aSu2n3B67dlleaCaTiTltzUKbO7023bo62fIyAftDAR6wOvyydeXrajbihQsX5s+fz5xjMm/ePPb3wvJkGRZG6XpjCwEuX77MDHJwcLj//vvZCyK3bdvGVMQOr8Dpyutt27b5+PiMGjWK/c21POWYmJh58+Y5ODgwlyGlpqa2n/KFCxeYk3qYc6TNlnNXMrfvtNC/ixNsT6FQEBF7zq1Op2M2QB0cHMyuKLVcCSwPNZspcxD9rbfeMllcK5gt+8OHD5uNzhyOnTFjRhffZlcW46lTp8LCwpi1KygoiDlI3K2l1H7KZu+LvVyt04XGuHDhwsKFC5lZy2SykJCQ9957LzMzs3349uMyR6ktf/RgZ8nJyYLk5OQpU6bc6eMHuKswx/9MXTi6BgDQEykpKTgJCwAAgAedn+EJcPdof+ETAEAvQQEGaMM+nQYAoLdhFzQAAAAPUIABAAB4gAIMAADAAxRgAAAAHqAAAwAA8KA/nQW968cDKpWK7xQAADAA+fl4hz3ysD3n2J8KsEqlWvHiC3ynAACAAWjz1h/sPEfsggYAAOABCjAAAAAP+tMuaIA+a8WKFUlJyWynRCI5e/aMUIh/cAHgjlCAAWzgROzJ8ZODRgeOJyKdTrt183/yS+sD/d35zgUAfZdd/0Pft2/flClTJBLJ9OnTr127RkRKpTI4OFgikQQHByuVSnuGAbCteb8Jff7FV59/8dXfv/Ay31kAoB+wawE+cuTIzp07tVrtG2+8sXTpUiKKiIgIDQ3VarWhoaFr1661ZxgAAAAe2bUAb9++fcqUKUS0bNmywsJCIoqJiXnrrbeIaOXKlVFRUfYMAwAAwCN+jgFHR0c/9dRTRFReXu7k5EREUqm0srKS26asvKKisoqXeAAAAL2NhwKclpa2bt26o0ePEpGF00RNJpPBZLRjLgAAAPuxdwGOi4t79913Y2JiPD09icjX11elUsnlcrVa7e3tzW05xM93iJ8vt09CUopdswIAAPQaux4DPnjw4IYNG2JiYnx9b1bWsLCw3bt3E9HGjRsXLlxozzAAAAA8susW8KJFi4jI1dWV6TSZTBEREYsXL37zzTdnzZp14MABe4YBAADgkV0LsMlkMuvj6ekZFxdnzwwAAAB9AW6VBwAAwAMUYAAAAB6gAAMAAPDAygIsEt128NhoNAYEBNgiDwAAwF2h2ydhMaXXYDBwa7CLi8uxY8dsmQsAAGBA63YB1uv1RCSRSLRabS/kAQAAuCtYuQsa1RcAAKAnrCzAe/bscXFxEQgEolskEoltkwEAAAxgVhbgZcuWRUZGmkwm/S3YJgYAAOg6K++EJRQKQ0NDbRsFAAaYv/71r8xZI4xx48a9+uqrPOYB6FOs3AL++OOPP/roI9tGAYAB5osv/n0tKT0xNTMxNfN47Jkdu39saNbwHQqgr7ByC3j16tVEtHbtWraPUCjEXmgA4BII6OPPvpFKZUR0OvbILzE/m4x4yDfATVYWYO5uJQAAAOgu3IoSAACAB1ZuAZvditJgMIjFYuyCBgAA6CLb7IJevnz5k08+aYs8AAAAdwXb7ILevHnzkiVLOm2m1+vXr18vEAjYPoLb2SQMAABA32eDAmw0Gg8dOtSVlnK5PCcnx6yniaPnYQAAAPoF2xwDlsvlO3fu7HQstVpNRNu2bbNupgAAAAMGz5chKRQKFxcXrVY7d+7cLVu2+Pv7s4NUzc3NzS02mQsAAEBfY2UBtpXGxka6dWx4yZIlly5dYgcVFZfm5OfzFw0AAKAXWV+An3jiiVOnTjU1Nbm6uoaEhBw8eND6ECLRmjVrPvzwQ27PCePGTBg3httn89YfrJ4FAABAn2LlSVhjxox58sknq6urTSZTVVXV/Pnzp0yZYsV0li9fXlBQYDQaN2zYEBQUZF0YAACAfsfKApybmxseHs48A1gikbz55psZGRlWTCckJGTBggUSiSQ6OjoyMtK6MAAAAP2Olbugx48fv2PHjqeeekoqlarV6v/+978TJkzo4rjcy43Cw8PDw8OtywDQfzU0NBQUFHD7jBo1ytXVle2srq4uLi7mNhgzZoyzs7Od8gFA77OyAGdkZCxevPi1115Tq9VOTk6hoaEpKSm2TQYwgJ0+ffqFZcv8/UcwncVFhZ9+8dUrLz3PNti/f//f3/mHr+8QpvP69bw9P0YtfPRB+0cFgF5i/UlYBw4csGEOgLvNPbPnrP/iO+b12395uUVtfmnfb0MfXb3mE+b1H5cubFXr7JoPAHoZnoYEAADAA2sKcEBAgFmfuXPn2iIMAADA3aLbu6Afeuih+fPnm/XcvXv3E0880ZNLgQGgV+n1+sLCQm4fd3d3d3d3nuIAQPcLcFxc3P79+816+vr6xsbG2igSANheUVHR+PHjhwwdxnQ21Ncte+mVL/71Cb+pAO5m1pyE5eLiYtbHaDTa6u7QANBLfP2G/ng4jnn97Vf/atHgOwvAp24fAx4xYkRaWppZzyNHjvj6+tooEgAAwMDX7S3ghIQEZ2fn8+fPz5kzh+lz6NChRYsWVVVV2TobAADAgNXtAuzk5KTRaJ599tnHHntMKBRqtdqgoKCGhob2+6XBChkZGUajke1UKBTDhw/nNqisrOR2ymQyLPm7U3Nzs0ql4vbx8PBwcHDgKw8AdJc1x4AlEgnuwtFLpk6d5iiVCoiISK/XBwSOu3Qp3lkmYYZqtVofHx8PTy+mU61ufex3T+zcsU3kgOu57zqffvrpP//5TydnOdNZV1sTfyVpZtAkflMBQNfx/DxgMCN0EEafuKRwcSWiX8+e/Gnf9laNwVnW1kAslhw5k8i8jt6/JyX5mtFoImz23JWW/uHVl/+8knm9eMH9qlYtv3kAoFuw5QQAAMADFGAAAAAeYBc08MxkMrW2tnL7iMVisVjMVx6APk6v12u1tx1ukEqlQiG2pvqfbn9mojuQSCS9kQ8GvKKiIrlc7nGLq5vbX9/+B9+hAPqur7/+2tXVlf3KKBSKk2d+5TsUWKPbW8C44xXYnN+QoT8fi2deb/nm36pWjYlIwG8mgD5sybPL/t/fP2Be/+GZxxqbcf5dv2SzvRZmlyR2SK/Xr1+/XiBo+2lVKpXBwcESiSQ4OFipVNoqDAAAQB9nZQGOjY11d3cXCAQCgUAkEgkEAh8fn07HksvlOTk53D4RERGhoaFarTY0NHTt2rXWhQEAAOh3rDwJa8mSJYcPH54zZ45EItFqtatXr544cWKnY6nVaiLatm0b2ycmJiY7O5uIVq5cGRgYuGnTJuvyAAAA9C9WFmCVSsXcC1oul6tUqnXr1nl5eS1btqy70ykvL3dyciIiqVRqdpPFq4lJyanp1sWD3vP999+//PLL3D4xR44/tuDBO7XXaDQymYzbZ2n4H7Zt/d5BiIO8AHBX6+llSH5+flFRUaGhoS0tLVaMbuHU+elTp0ybMpnb5/sfdlkxC7Atk8n0xJO//9v7/2Q6Vyx7sq5JbXkUsVgSl5DPvD74067MtBSj0eggxO27AOCuZmUBHjNmDPMiPj5+2LBhKpXq+++/t2I6vr6+KpVKLper1Wpvb2/uICGua+urmGP/7OsujtKt9gAAA56VNe7q1avMC7lcXltbq9Vqw8PDrZhOWFjY7t27iWjjxo0LFy60LgwAAEC/Y2UB9vHxGTly5NatW7ty9ZEFERERO3bskEqlx48fj4iI6MmkAAAA+hErC3BjY+O5c+eSk5NHjhw5fPjwTZs21dXVdXFck8nEvvb09IyLi1Or1XFxcZ6entaFgZ545NFHXTjGjZ/QqsG9VswNGTpUInHk/l1KzOI7FAD0b9YfZvX39//iiy+USmVUVNSOHTtQPvuppsamD/753+jYK9GxV77dGdXQ0NiMp9q1YzKa/vR/fzt+PoX5E4vFLRoj36EAoH+zvgDfuHFj2bJlbm5ujz322OOPP15eXm7DWGBPTk5OznKFs1zBPt0d2nN0lDJLyVmuIJxKBgA9ZuVZ0HK53NPT84MPPvjyyy9dXFxsmwkAAGDAs7IAe3l5FRQU2DYKAADA3cPKXdCfffbZP/7xj/71+IRnnnnG2VnO/Tt4+DjfofocrUYzefxoP78h7N/eyAN8hzK3aPFibsKZs2artThxDGwjICCAu3Yte3G53tDXj/f/+ZVwbuY/vPSyoc9nBurJvaCJaMOGDWwfoVBo9ozovqahoeGRx5e89MqbTOerLy5pbsU6as5EphGjAtes+5zpXL/27bKqWn4jtVdVWfV/f1s7afJ0IqqsKPvHX19TtWilkp7e1g2AiEpLy/ZEnXKUOBLR+XOxly+c0+mNIoc+fVug2pqaHw+dFYslRBR35sTVy79q9UZZ384MZHUB7qdPBXZ2dvb0vvnUJpFIzG+YPkvi6MguJUeplN8wdzJo0GAmpN7QL1dF6Mu8vHwkjo5E5OI6iO8sXeXh5SORSIjIxdWN7yzQVfgXCQAAgAfWF+Cnn37azc1NJBIR0ciRI/ft22e7VAAAAAOclbugJ02atHfv3r179zI7Pc6cORMUFPTMM8/YNBuAlR5esOD69UK2c5DboLq6OuJcu/v991vnPnAf2/n1119//sW/uVM4GH1owtjRvR60L9mzZ88rK1Zwn1L10suvfbbxYx4jAQxsVhbg9PT0SZMmsZ3+/v49vCk0gA3l5eX/ZfX7vkP8iSg3K+OrLz6eODno5T+vZIa+9/YbxRW3nVlWXV09ZfrsZ55fznT+5ZWlFcr6CWPtnJpnjY2N7oM9P920len89qt/CSUyy6MAQE9YWYAnT54cGxv7wAMPEJFard6wYcPcuXNtGgygR4b6j/AfPpKIVE1NRKRQuIwYeXOLVurYwZllbm7ubAOR+C49QU8icWQXgsLFld8wAAOelceAU1JSduzY4eHhQbduynHy5EmbBgMAABjIrL90cvv27du3b7dhFAAAgLuHlQVYJBJxLwU2Go2BgYH5+fk2StUnVFVVPfrYY9yHJz63NHzlW3/hMRLAXaWkpOSJJxaZqO07+OJLf3z9T6/yGOnulJCQ8MorK7gfxKrVf3/26SctjPLY735XUVHBdk6bNn3z5m/6+P1M7K/bBZi57shgMDAvGC4uLseOHbNlrj5Ap9MVFt7411fbmM5DByPTMvNNJpMAT8IBsAu1Wl1aVvbJF98ynQcid6ZmDqj/8vuLpqamVo129Zr1TOeWb/6dlVdkeZSkxKS/vvux+2APIspKTz1xNKpVo1c4SXo9a7/S7QLMbPhKJBKb3HjSrJhxNzf7ArFINGHSNOb15YtxLc3N/OYBuNs4OkrZ7+D5M7H8hrmbOTvL2Q/CzX1wV0YZM26il7cvEbW2tvZisv7Myl3QNrztc18rugAAAHZg5R75PXv2uLi4CAQC0S3MHTkAAACgK6zcAl62bFl0dPSCBQt6OHuFQuHi4qLVaufOnbtlyxZ/f392UE5efkHhjR5O37L1H77z7aa2Bzo9GPrwP/7+dp86xKusqngi7BGRw81IJpOR6K7bYZCVlfXaa3/i7impb2jgMU9/8fnnn0dFRbOdanVrD1ee8+fPv7vmPeJ8EGsi3v/tb4J7Ms2+r7y0+OHQh4ScX4Ufdu4cNnRI783x7NmzEe+v5S7niLUf/CYYN1oYgKwswEKhMDQ0tOezb2xsJCK9Xr9+/folS5ZcunSJHeTl6eHo6MhtfKO4pOdzZJlMpsy05E3f7WU6L54/fflqkk5vlIgdLI9oTxq1WuHm/vji3zOda9/5P37z8KKxsbGouOSv//iI6dy383u1uk8/+LKPyMrK9hseODfkIabzL68+7+3t25MJVlVVNala/vinmzcU2/zlxvScG7/9TU9z9nGt6la3wd6PhN084/fdVX8uKqvt1QJcVVXV3KJ56dWbX/av/7MhI+cGCvCAZGUB/vjjjz/66KM1a9bYJoRItGbNmg8//JDb083V1c21d+/FIxAIZs6ew7wuLytJunbJcnte+Pr5syGl0rv01oByhYJdCKdPHCm+cZ3fPP3F8BEB7HLj3uTZau6DPdgJ7tu1pecT7Bf8hg5j37XZVkEv4S5nNzd3O8wReGHlMeDVq1evXbtWxGHdMeDly5cXFBQYjcYNGzYEBQVZFwYAAKDfsXILmHsXjp4ICQlZsGBBQUHB7NmzIyMjbTJNAACAvs/6W1HaRHh4eHh4OL8ZAGzOZDK9unypzLHt+3X9emEz54lhAqFw1Oi77HFLfdLatWu3bN3GPfHSZDLyluYO9u7ccjS67YHrarXG02dYTyb45ZdfHjt+nNvnxx9/kkntsXe9i1Qq1e9//xz33luPPvq7115b0YdOkbUFK++E1Z5QKLThxcEA/ZrJZCrIy3195btM54F9OyoqKn7/wssjA8YQUU111eYvP8UV8H1BRkaG75DhTz33B6bzP59+2Ac/lazM9BWvrxo02IOI8nOzYn7e18MCnJiY5Oziec/985jOt//yckVN08ghfagAa7Xa06dPrd2wiemMO3Mi7uLVFa+87DCwbmZp5Z2wAMAyhavbvN/cvFIg/tczWRkp02bMnho0i4jKSoo2f/kpr+mgjd8Qf/aT2va//5SX2fJqC1uZPSfYx3cIESkULjE/7+u0fafGjJvIvmuhsC9uWIrFEjZhWUlRWWkxv3l6w4D6bwIAAKC/QAEGAADgAc8nYQ0wH330UXp6BttpNBoFt+/cee1Pf577wP02nGNJUeEL4eHsTDQajYODA/c4/e/Cwp77/bM2nGPPFRddDw8PF96641hzc7PZwdBDP0f6HNjLdhqNBt8hPTri1V0mk2n9h+99N3gQ20erw/kNHYjavzf+bNtj0EYHBr7/foSwy/eSU6vVy5cv53768+f/dvkfX7IwflpywnPPLWU7pTLpt//7lntcMCLi/dzcXO4oJiLuBP/yf2/NvmdmFxNCF23ZsuWTTzYQ56Pn/ZSgzMzMD9et4978bfkfX/7t/BC+8nQIW8C2dOzYcanCY/y0+8ZPu89vxLhjx44nJqUwneOn3ZeakRWfkG7bOTY1NjS16thZHD58+PiJE2xnVW1j7JmLfe1kH7PMvxz7xSyhTqcLeeix11e++/rKd1e8+XZDY6PRaO+3cPZ0LJuwWWPU6w12DtAvpKUkeQ8bwywlZzfv6JgjqpZu/Ozq9fr9+w+wy7mpVX/s1DmDwdJJyEplhUDszLQfNS5o375IZX0Lt8HRo0fl7r5MA6+ho0/ExqamZbCzSExOvZyUaeW7hTtLSUkROIjDl7/O/AmEIiPfPzsVFRWXL19lP/qs3IJfLyfzG6k9bAHb2D33z5sx6z4iqqos//7rL7y8fRb8bjEzKO7Mid6Y4/iJU9hZ/PPDv0ulMrazvKxE3ScfBDZh0jQ25IYP/ta+QdDMe38b+hgRaTWaTzpq0NuEQgc2YWtry9lTA+1x17YSPD90yNDhRJSceOVK/Pnuji4StS1nVVNTQX52p6MEzboveP7DRNTSrPr8n2vbN7hvTsikqdOJqPjG9V3bvvH1G8LO4hUxcQ0AACAASURBVOSxQ91NCF3kw1nOx44crFZW8puHiDw8vdhIVqycdoAtYAAAAB6gAAMAAPAAu6DblJeV/PlPf2JPaGpubrZ8EKOoqOjjjz/mHulo4tzqqEOxxw7lpV9jO4cNH/7O3//Wpx6A2N7xozHZqVfZTqVSKRDdpc+EYJlMpi82frDXw43t0/NTTn45fDAzOZ7trFIqRY7O3Yr0+afr93gOZvsUFFx39xlpYZSs9NQVK15lO83OXRqoDkfvT7v2K9uZlZUdMHZyTya4a9euc+fi2M7W1lZHqaNQ0LZt87uwx8N+9yjbmZeXt/HTT7knBy19fum8ubZ82JGyquKN1//swDkB9KOPP/YY3I2HOnz11X9TUlLYztraWhvGY/z5z69z7yohEom4nRqNxnQXPHoVW8BtGurrrheXufuMZP72799v+fQlpVIZc+gw2/5aUmpjU7PlWaQlJ5pEzkx7jVG8a/e+hmaNTd+E7aUkJZjEciaz2iC6dPnKwP9adM509uRx9qPPyM7X6np6g5qkhMsCRxdmgq164ZWrV7t7FsvRQ1FspBsllUUlpZbbV1aUVtc3M+3l7n7nz/fFg2Q2l3Al3kHqxrzrZi0VFff09g6nT58pKlOyS3737l0HDvzMdqZl5h45fpbbvry8/JdjbSvPpSsJJ89d6WEGM02Njbn5hews9uzdm11Q1q0pHD5ypLZJzYzu5OZz5OgRm59T9e23/3P1GsbMoqKm8ZfjJ7Lz2jLv37+f77O47AFbwLeZGjRr8TM370391ecfd9re3X0w277wet7li3GW2xPRQ488PmJUIBFlpid3pX1fEPrIwuEjA4goIy0p9pfoTtvfDZzlcvajr62tzs6ywfntDz+2aKj/cCJKTbp26sTh7o7uIBKxkYjoekHnW7T3zgkJefARImptbfnyXx91d4791ILfLfId4k9ESQmXD0f92PMJTp917xNLbl4c9a9P3lMoXNgPoqqqvH17Ly9vtkFmRkr7Bj03cXIQO4tt335pxRTunzv/geAHiaipseF/X/XKjdsWPfU8c82k4qhrWvK1iVPaMn/39edabV/fOOk5bAEDAADwAAUYAACAB/14F/Sn//pXZUXbpWZGo0Ho4MA9bK/RaBwd257vUVpa6j00oCdzvJ6fs3r1ava+OkqlsidTI6LW1pb33n3HUdyLn0JBXjY3c2trq0wm5d4aqLm5k+PWndq/b1fy5XOcHrfdeshgMFAvn0yh1+vej/iHTCJu66PTWR7lp327Ei+1HZnLz89z9x7eW/lsJHLPjmsXT7OdeXm5nn6jenWOSdcur1q1mu2sqOhgbypXc7NqzT/+Lrnz+lxbW/3emnccxTc/KZ1Oa3acr6yk6O2332bvpVVfX2d55TGZjB++/66TVML2aVWrLYfsIZPJ9N8vP4vy8WT7FJcUew8bY2GU7Kw07mKsqqoya3Al/vyqVRVsZ3l5947XdorJfNDbg+1TUlIyZOQEbptPPnrfxdmJ7ayvr7M8zcsX41atalsfrl27JpQ4WWivUjW9+4+/S0QO3FRdzM8oLrr+9ttvs6estrS0yGRSAedkN4GAuJNsv5zjL5xbtartxAhvb6+Vf/0rv2fA9uMt4O+++768ulFjctSYHEsq6/bsjTxy9DjTqTE57t0XuW379oZWI9OZU1BcUtrJz0enKspLUzPzmQm2GkQ7duzo4Q2aNGr1qVOn2cx79kb2MGF75WWlaVkFzPRb9A6bN3+zY+dudo4nTp7p9MSxTp345VCThpgJZuXd+Gn/wbPnL7Kz2LptW2+fS6HX648eOcLO8WB0jLazAnzsSDSbOTO3MDE5tZcz2sAvh6NUGgGTOSP3elJKWm/PMS8n80apkpljVV3L0V+OWf7NVLe2nDl7jv0gdu7abdagsb7u8pUEtsGWrdvMznStrlYmJme0rTxbt1q+oZLJaDr48wG2/S/HY1XNLRba24Lpp8i2b9CVxNTCG508PamkqDAr7wbTvklDP/70o/H2m31lpKcUldcwDSprVceOx9r2BGCT6fbMCSk3ikvNGvy4by/b4EzcheraesvTTE9LLq6oZdpX1DSldLY2tjSrzp6LY2fxw46d3X0X1VWVSWlZ7BS++ebrrdu2s52nz/16MPpwTkEx09nQavxp/36zlSc9JbGkso5pUF7d+N9vvq1r5Pk+RTxvASuVyiVLlly8ePG+++776aefPD09Ox+H4/HFzzIPWM3KSD178pfRgePCX3qNGXQh7lRDQ/3Tz73o6jaI6Tx32gY3opob8lDoowuJyGDQf/3vf/Z8gqPHjG/LfO6kUllhub0V5v0m9MEFYUSk0+n+t+lTTy9vdo6VFWVXbXGDmGeWLpcrFEQUd+ZEWnLC5KnT2Vkc/GlXc3MnV2f13LDhI9k5ZqQmpqcmdjrKs88vd5YriOjsqWNdad8XPPvCH52cnIno7MlfMlKT7DDHBb9bPHnaDCIqKb5xOKrzfxDHjp/EfhBnTh5tfzukqdPvYRv8tHd7fV2NWYPZc4IXP/0883rzpo2dztHb14+dYElRYeK1eMvte04ilrBz/HHPtqifzP/PaO83Dz06N+QhIlI1Nf3w/VftGzwS9uTEydOIqKiw4GjMAZvmJSKSSBzZzJG7HKM591pnuLkNYhuomhrPn4vtdJqPPv7k+IlTiajwel70fvMJtjd+4lR2Fid+ia6t6fYexPse+M3ji2/e2f6/X6znZm5sqL8Qd+o3Dz02Z958pnPXts0dZV4ybsJkIrqen3Mh7nT7BnbG8xZwREREaGioVqsNDQ1du7aDu8oBAAAMSDxvAcfExGRnZxPRypUrAwMDN23axG8eAAAA+xAkJydPmTKFr9lz734ikUi4txOqrFIqq6u5jX+9dGVW0DS28z//+dLHb6jMyZmImlVNxTeuO0qlzB5pIsrKSNVqNOMnTRWLxURUX1dbXFTo5ubuP3wE0yAtOUGtbp05ew7TqayqbGqsd3ZWePv6MX0SrsY7CIVTp9/DdJaXFqvVrS6ugwZ7eBKR0WhMuBLv5OQ0YfLNSDcK83VanZe3j4urGxFpNJqczDSpTBY49ubJDvm5WTqdbviIAJmT063MhY4y6chRgWzmlpbmKVNnisQiJrOyqkLm5MxcG0pEqcnXNGrNzNn338pc0dTY4CxXePvcynzlooNINDVoFtNZVlqsbm11GzTIffDNzIlX42VOzhMmTb2Z+Xq+Tqf19vFTuLgSkUatzs3OcJRK2cx5OVl6nXb4qNEymRMRqZqaSooLpVLpCDZzeopGo544ZTpzPV9dbU21svK2zEnXNBpO5sqKpqZGZ7n8jplLimprqv2GDnMf7EFEBoMhOeGyVCabMOnWcr6ep9PpOJlbc7Mzb8+cqdNpR44aI5XJiEjV1FhSfIObOTM9RaNWT5o2XeTQceaUxKs6nXbGPTczV1WWV5aXefn4spmvXb4gEovZzKUlRQ31dT6+QziZr8hksvG3lnNhQZ5K1Th8REBb5pwsR0dHNnNudqZepx0Z0Ja5tOSGo6NsxKjRNzOnJWs06knTZnAzOzk5D7mVOTnxil6n42ZWNTXJ5QovH182s1gsmRI0k82sUasHubsPcm9bzhKJI/MYAyazTqf18RuqULgQkVrdmp+T5SiVjh4zns2s02lHjR4jlcqIqKmpsaykSCqVDh/ZlrmlpXnajNkODg5EVFdbXaNUypydhwwdxmY26PXTZ913M3NFuaq5SS5XeHm3ZZZIJJOn3cpcfEOjUQ9y9xjkPpiI9AZ9auI1mUw2buIUbmZfv6FyJnNra35elqMjN3OGTqsNCBzryGRubCi8nieXu4wMuLluZKQlq1tbpk6/h8lcW1NdW6N0cnL2YzMnXDEY2jJXVpQ1q1QKhYuntw8nsyOz356ISopvaLmZ9fq05GtSmWzchJuZrxfk6nU6Xz9/5iBOa2tLQV6OVCoNCBzHZtZqNaMDxztKpUzmstJiqVTGXJpPRBlpSerW1mkzZguFQiKqrVHW1tQ4OTv7DfG/lfmywWicPvPe2zK7uHh63cx89fIFR0fHyVNvy+w+2NNtkDsR6XX6tNQEqVTG7Lwlouv5uTqddsjQYcxBnNaWltzsDKlMNmbcRKZBTla6VqsJHDuROQ22saG+oqxEKnMaNuLmaYMZqUmtrS1BM+9lMtdUK+tqq52d5b63MiclXDYZjUFs5vKylhaVXOHq6eV9M/OlX6VSGbu6FhcV6rQaNrNOp0tPTZRJZWPbMufodDpO5ubSkqJXX/uTzLHt5M0riUkrXnyB7CUlJYXnAswtumYF+EZxSUnZbadNZWbnGAx4KhwAANieQuH83JIn7Ta7lJQUnndB+/r6qlQquVyuVqu9vb25g4b7Dx3uP5TbZ87sWfZNBwAA0Ft4PgkrLCxs9+7dRLRx48aFCxfyGwYAAMBu+D8LeseOHVKp9Pjx4xEREfyGAQAAsBued0F7enrGxfWPBxIAAADYUD++ExYAAED/hQIMAADAAxRgAAAAHqAAAwAA8AAFGAAAgAcowAAAADzg+TKkbtn14wGVqtcfbAcAAHchPx/vsEcetucc7VGA9+3b99FHH2VlZU2aNOnbb7+dMWMGO6hbzwNWqVT2vFM2AADcPTZv/cHOc7THLugjR47s3LlTq9W+8cYbS5cu5Q7C84ABAODuZI8CvH37duaBS8uWLSssLOQOiomJeeutt4ho5cqVUVFRdggDAADQF9j1GHB0dPRTTz3F7VNeXu7k5EREUqm0srKSO6iouKS0vMKGcy8sLMzJySGBgO0z5/77nZ2dbTiLnjtz5oxWp2M7PTw8pgcF8ZinvdLS0vT0dO5inDVz1qBBbjacRUpKSgVnZRAKhQ/+9rc2nL4VsrKyioqLuX3m/2a+SOTAV57e0NDQcOnSZWr7YGn8uHH+/v78JepcfX395ctXuJknjB8/dGjbU9SqqqqSk5NNnFGCpk2zfKir7ysuLs7MzOR+B2ffM9vV1YXHSJWVlSkpKdzlPD0oyMPDw8IosbGxRlPbGD4+PlMmT+61gH2U/c6CTktLW7du3WeffXbb7IV3DCBxlDg7O3H/ehigpKQkM+e6Widg/s5fuFxaWdvDadpc3PkLTS16JmFZRe3FS4k6fd96BHJlZWVqRi67GOMvJxaW2PL/JCLKyMwqLlMy02/RmGJPnlW1aDsfrTfl5+cXFJay7/rkqXP1TS38RrK5xsbGK9cS2feYmp6TkX2d71CdaGxsvJqQxGZOScvOyLktc01NTVJKBtvgWmJqXmEZX2ltpby8PD0rn31TF+OvlVZU8xupurqau5yvJqTkd7acz5w736olpn1RadWlK0l6g9E+afsOO20Bx8XFvfvuuzExMWb/e1p4HrCPl5ePlxe3z8XLV3sYw9fPb+as2czr9LSUHk6tl0yfMdPRUUpE1wvykxIT+I7TAU8vL3YxFuTn9cYsAgICx4wdR0R6vT7+wvnemEV3DRs+clrQdOb1xb4RyeYUChf2k22or+c3TBdxM9fX1bVvMMjdnW1QWlLcvkF/5O3tzb6p7KxMfsMw3Ad7sJGKi4q6MsqMmfcw22DZ2Zl5Odm9GK6vsscW8MGDBzds2BATE+Pr62s2CM8DBgCAu5M9toAXLVpERK6urkynyWQiokmTJqWlpUVERCxevPjNN9+cNWvWgQMH7BAGAACgL7BHATaZTO17pqWlEZ4HDAAAdyvcihIAAIAHKMAAAAA8QAEGAADgAQowAAAAD1CAAQAAeIACDAAAwAMUYAAAAB6gAAMAAPAABRgAAIAHKMAAAAA8QAEGAADgAQowAAAAD1CAAQAAeIACDAAAwAMUYAAAAB6gAAMAAPAABRgAAIAH9ijAer1+/fr1AoGg/SDB7ewQBgAAoC+wRwGWy+U5OTl3GmrisEMYAACAvkBkh3mo1Woi2rZtmx3mBQAA0C/wfAxYoVC4uLhIpdKHHnqouLiYO8hkMhlvx1dIAAAAm7PHFrAFjY2NdOsg8ZIlSy5dusQOupqYnJSaxl80AACAXsRzAWaIRKI1a9Z8+OGH3J6zpk+bNX0at8/mrT/YNxcAAEBv4XkX9PLlywsKCoxG44YNG4KCgvgNAwAAYDe8FeBJkyYRUUhIyIIFCyQSSXR0dGRkJF9hAAAA7Mx+u6DNrjJKS0sjovDw8PDwcLtlAAAA6CNwJywAAAAeoAADAADwAAUYAACAByjAAAAAPLCmAItEt526ZTQaAwICbJQHAADgrtC9s6CZ0mswGLg12MXF5dixYzbOBQAAMKB1rwDr9XoikkgkWq22d/IAAADcFazZBY3qCwAA0ENWnoT19NNPu7m5MTuiR44cuW/fPpumAgAAGOCsKcCTJk167733amtrmc4zZ8689tprNk0FAAAwwFlzK8r09HTmTs4Mf39/lUplu0gAAAADnzVbwJMnT46NjVWr1USkVqs//PDDuXPn2joYAADAQGZNAU5JSdmxY4eHhwcReXl5FRQUnDx50tbBAAAABjIrn4a0ffv27du32zYKAADA3QO3ogQAAOCBNQX4wIEDzL0nr1y5IpfL/f39bZ0KAABggLNmF/SKFSsuXrxIRE888cSJEycUCsWQIUNKS0ttnQ0AAGDAsqYA19XVjR49urGxsbW19b777iOiyspKWwcDAAAYyKzZBe3r65uVlfW///2Puf9GUlKSp6enhfZ6vX79+vUCgaD9IKVSGRwcLJFIgoODlUqlFWEAAAD6I2sKcHFxcXBw8L///e+PPvqIiJ588snNmzdbaC+Xy3NycjocFBERERoaqtVqQ0ND165da0UYAACA/sjKy5C4+5zz8/MtN2Zu2bFt27b2g2JiYrKzs4lo5cqVgYGBmzZtsi4PAABA/9K9AhwQEJCfny8SiZjnEvZceXm5k5MTEUmlUrMDyaXlFRWVVd2aVGZmJrePWq2WSqVsZ2JioshRcf36daazprpGq9Vw2+fm5hYXF3P7zJs3j/vk4/T0dG5IoVAYEhJiIVJNTU1ycjK3z6RJk7y8vLr4joiotrbm9OnTIoe2HRX33nsvs8R6KXPPFRYWFhQUcPuYZTajVqsvXLjA7ZOWlmYgiVjiSEQGg6Guvt5slISEhHpOT5lMxpyLwIqPj29paWE7XV1dZ8yY0f230qa0rEwolru6DWI66+rqjEajWeaqqrbV1WzdIyKtViuRSLqe2aw9Ec2YMcPV1bUn78L+zp49azAY2E4vLy/uXWzby87O5p7OqdFoJBIJ9+jVqFGjRowY0ZNIaakprU01bGf75Wz22ZllNhgMZ8+e5bbX6XRisZjbJyQkRCjsxs7Fq1evNjY2sp1OTk733ntv10fvlF6vP3fuHLePv79/YGCghVFSUlKqq6vZTrFY3MPbHZaUlJjtB9XpdBbad5q5paUlPj6e2yAgIGD48OE9CWl/3SvA77//vkgkMhgM3J94IhIKhdY9o9DiamoymYx3HmqusrIyITk9YPQYpjMtNaW6WvnAA/NEYjER1dXVXr6aOHbCNLX25s9BdW1dfUMzdwp5eXkFN8r9hgxhOi9d/HXi5CBvz0Fsg/SMzIamVg9PLyIyGo2XLv4685775U63fXu5amtrL19NGjt+ItOZnZUhlrp0qwDX1dakZeaOHDmK6Uy4dmXYyDGjR7YVs7y8/IIbZbdlnjLd28ONbZCWntGoUrOZL8dfsJy554qLi1MzcocNH8FmHj5qbMCIOxZgjUZz7vzFqUEzb41elJmd6zd8LPNJ6fX6mpq6VrWOm/natUSJTOHi6kpEarU6J/vK1KCZTtK2H8ELF+J9ho6QyWRE1NTYmJCcMWnyVEeJlft7iKi8vNzZ1YddeWpqalWtGu4HmZqarlLrPDw8ichoMJw6dcLT02vqtOnM0Py83IqysslTp7GZc3OummU+/+tFP/+RbObEhKu+Q4YGBt5cn1OSkzy8h07pbwX49Jlzk6fOEDo4EFF1tTK3oHjc+AncfyjN5OTklJRX+/j63Rz9ZKxc4TLrnpvVqOhGYV2TpocFODMjQ65wYUpsY0NDUlLCkCFD2N+NlKTE6prqkJD5bOa86yXczHq9/tSZczNm3fznqbysrKAgb1TAaN9bmS/+Gjdtxmx3V+euR7p6NcHZxV2uUBBRa2vr9YLEqUEzZY7Wr65m9Hr96bNx02feXIxlpaVlVfUBAaOFwg7Oy2GkpKRpDOTuPpiI9DpdUlLC9JmznWXW/26UlpYmpWaOHDWa6UxOTGhpUVtor9PpzDKXKxsCRo8W3vpvrKWl5fyvlybf+ordKLze2KIf4AU4PDw8PDxcIpHY6pHAvr6+KpVKLper1Wpvb2/uoCG+vkN8fbl9riWlWJ6ap6fX7HvvZ14X3SisrlbOmHWPVCojosLrBceOHnZ2cho69OZVyw4ODu2nMGLkyKDpNyvBtauX2zcICBwzbtwEulWAO32DboPc2UjVym5s0LOGDBnKTiEzI81y5qtXLrVvMHrM2LFjxxORwWC4HH+hfQOb8/MbwmbOSO8gsxlHR0e2vclkIiI3Vzfmk9LpOl7TJkycPGToUCJqamzMyc5q32DatOlugwYRUUV52amTJ6x5G7dTuCjYlUcg6KCEjBkzLnDMWCLS63SnTp2QKxTsm2pWqSrKyiZOmuw3ZCgRNTY05OZkt59CUNAMVzc3IiovK01MuOrl7c1O4XpBJwd6+qxZ99zL/BOcm5OdlZneafuRo0ZPmTqNeX32VKxUKmMXgpGzMd0TQUEzmP+ESktKkpISvL192Vnk5+VW11TPmn0fs42Rk52Vk51pNrpIJGLbJyUmFBTkjeJk7srPQnsTJ01m/u2oq6vtjc/6tswJ12rrajsdZezY8aMCRhORRqNOSkroeQYfXz82Q25Odk1NteX2YrGYbZ+YcLW+3Z4wmVPbunGnH4o+rnsnYTH33zDb+dYTYWFhu3fvJqKNGzcuXLjQVpMFAADo47pXgLm7oLnMDqJ0BXNYJSIiYseOHVKp9Pjx4xEREd2dCAAAQD9lv13QzK5FVlpaGhF5enrGxcV1d1IAAAD9nTXXAdvqADAAAMBdq9sFOC8vb9y4cU5OTgKBQC6XT5kyBXewAgAA6K7uFeAjR44EBgZ+9tln1dXVJpOptrb2s88+8/LyMrswDgAAACzr3jHgF198sbCwkL3WSiKRPPjgg9nZ2XPnzsXzGAAAALque1vAVVVV7a90HjNmTE1NTYftAQAAoEPdK8A+Pj55eXlmPfPy8iw/DQkAAADMdK8Ab926NTAw8NChQ8zzFVpaWqKjo5k+vRMPAABgYOreMeAFCxaUlJQ88sgjzz77rFqtdnJymjp1anV19eDBg3spHwAAwIDU7ft9DxkyJCWlk3syAwAAgGXW3IgDAAAAeggFGAAAgAcowAAAADxAAQYAAOABCjAAAAAPUIABAAB4gAIMAADAAxRgAAAAHqAAAwAA8MAeBVipVAYHB0skkuDgYKVSyR0kuJ0dwgAAAPQF9ijAERERoaGhWq02NDR07dq1ZkNNHHYIAwAA0Bd0+17QVoiJicnOziailStXBgYGbtq0yQ4zBQAA6MvsUYDLy8udnJyISCqVVlZWcgcpFAoXFxetVjt37twtW7b4+/uzg64kJiWnptshHgAAgP3ZowALhXfc0d3Y2EhEer1+/fr1S5YsuXTpEjtoxtSp06dM5jb+7oddvRcSAADAnuxxDNjX11elUhGRWq329vZu30AkEq1ZsyYxMfG2ZEKBw+3sEBUAAMA+7FGAw8LCdu/eTUQbN25cuHAhd9Dy5csLCgqMRuOGDRuCgoLsEAYAAKAvsNNZ0Dt27JBKpcePH4+IiGB6Tpo0iYhCQkIWLFggkUiio6MjIyPtEAYAAKAvsMcxYE9Pz7i4OLOeaWlpRBQeHh4eHm6HDAAAAH0K7oQFAADAAxRgAAAAHqAAAwAA8AAFGAAAgAcowAAAADxAAQYAAOABCjAAAAAPUIABAAB4gAIMAADAAxRgAAAAHqAAAwAA8AAFGAAAgAcowAAAADxAAQYAAOABCjAAAAAPUIABAAB4gAIMAADAA3sUYKVSGRwcLJFIgoODlUplFwcBAAAMYPYowBEREaGhoVqtNjQ0dO3atV0cBAAAMICJ7DCPmJiY7OxsIlq5cmVgYOCmTZu6MggAAGAAs0cBLi8vd3JyIiKpVFpZWdnFQZVVyqrqavNJcdpkZ2er1Wq2s7q6uqauPi7uDNPZqm51kjvHx//q4CAioqamRjf3QdU1Vb/8Es00kDiKUpITVA1tEywpL9fqSdWsYjqFQsG5uLMKuVPbLGpr65talMoqIjIZjSKJ+OSpWEdJ2zLU6/UiUVtnXV2dqrmJjdTQWJ+VndmsqmUb6HQ6sVjMfYN1DfVHjsQ4ODgQUVNTk8BBWFFZzk7BaDLEx1/Iy3Vj25eWl2n1Ajazg4PwXNxZhbOMbVBbX9fYrK6qqryZWSyynLl9JK1WK5FIblvONQ3c5ZyYlFBZXsQ2qKioaGxWczNfjL+Qm+N6p1mo1Wqjyci2V1ZVypxkGRnJpWVFRGQwGp3lTmfPnpY7t2VQtbakpiUVXM8jIq1WYyRj7KlYicih7U0ZDVevXXZ0dCSiluZmjVZzIjZWJGrb32P2pswWgslk0uv13JC19fUt2pzGxnqm08lJeuHXczmDXNgGBYXXSyqqMrPSichoMAoEQq1Ww76pquoqnUF3Lu4Ms7ZrtVpVc1O7zMYrVy+xmZ2cnWpra9gpaDTqhISrZaWFd1qMJpPJYDBY+Cj1er2Dg4NAILjTu66qqiqvKI+OPsB0VlaU19RWm4xtXzGzhdbhLLgTJKL6poZDh6KEDkIiampqbG1pOR57QngrQ/vMFVVVemNNw63lLHWWkcDUthgrK0xk+uX4cbZ9Q0NDq7qVbVBdW93cqvpF38o2qKura2xsW11VzU1Ozk5XrsZLeYgK9AAAIABJREFUJI5E1NysEggF+QW5zdHNTIOauhqZk+zXX88KhQ5E1NhQ39DYwM2s1+uFQiE7wZrqapmT7HphPptZJBadPnvaWXrHtUuj0TCfMqtFo05JScrNy2GGGoyG2JOxYs7qaracq6qqautVbAadXnvlyqWiG3l3mqNerxfcnlmjUR87cZxdGXQ6nUgk4q4b9U0NmVnppWUlRGQw6IUOwpOnYiXiO/5uFBcXF5e0rTzllWWJidfqaivYBpWVlfWNzWwGvUHnLHc+H3dGIBQSUUN9ndly1ul0JBS0fbLVSp1We+x4W+bm5ma9wcA2qKgodxAKuetG+9XVLLNUKh07dizxSpCcnDxlypRenYdEItFqte1fWx50o7iktKycO52snFydXt+rUQEA4O6kUDg/t+RJu80uJSXFHlvAvr6+KpVKLper1Wpvb+8uDhruP3S4/1Bun/tnz7JDWgAAADuwx0lYYWFhu3fvJqKNGzcuXLiwi4MAAAAGMHvsglYqlYsXL75y5cqsWbMOHDjg6elJRJMmTUpLS+twEAAAwMCWkpJijwIMAAAAXCkpKbgTFgAAAA9QgAEAAHiAAgwAAMADFGAAAAAeoAADAADwAAUYAACAB/a4E5at7PrxgEql4jsFAAAMQH4+3mGPPGzPOfanAqxSqVa8+ALfKQAAYADavPUHO88Ru6ABAAB4gAIMAADAg/60CxoAAO4Gra2t7733nsnU1mfu3AcG3gN7sAUMAAB9S2tr66ZNm3QCGfN3JSFl7/5DBoOR71w2hi1gAADoc6RS2fMvvsq8FolEZaXF/ObpDdgCBgAA4AEKMAAAAA9QgAEAAHiAAgwAAMADFGAAAAAeoAADAADwAAUYAACAByjAAAAAPLBrAd63b9+UKVMkEsn06dOvXbtGREqlMjg4WCKRBAcHK5VKe4YBAADgkV0L8JEjR3bu3KnVat94442lS5cSUURERGhoqFarDQ0NXbt2rT3DAAAA8MiuBXj79u1TpkwhomXLlhUWFhJRTEzMW2+9RUQrV66MioqyZxgAAAAe8XMv6Ojo6KeeeoqIysvLnZyciEgqlVZWVnLb5OTlFxTe4CUeAABAb+OhAKelpa1bt+7o0aNEJBTecRPcy9PD0dGR2+dGcUmvhwMAALALexfguLi4d999NyYmxtPTk4h8fX1VKpVcLler1d7e3tyWbq6ubq6udo4HAABgH3Y9Bnzw4MENGzbExMT4+voyfcLCwnbv3k1EGzduHHgPWwYAALgTu24BL1q0iIhcb23XmkymiIiIxYsXv/nmm7NmzTpw4IA9wwAAAPDIrgXYZDKZ9fH09IyLi7NnBgAAgL4Ad8ICAADgAQowAAAAD1CAAQAAeIACDAAAwAMUYAAAAB6gAAMAAPAABRgAAIAHKMAAAAA84OdpSAAAAF2XmnRtxMiRgluder3eQeQgILYHvf6Xt1av/D9eslkNBRgAAPo6vV636OkXHlwQxnQuXnD/kKHDvvxuL9O5Y8t/i0qV/KWzEgowAAD0A65ug3z9hrKdIpGI7XR2VvAUqkdwDBgAAIAH2AIGAIB+r1pZGRsby3aKxeLg4GAe83QFCjAAAPR7Vy/9mpxwadCgwUSk1+tysjOv3ygb5CLlO5cldi3Aer1+48aN77zzDvtcQoFAwG3Q/nmFAAAAnRIKhSveeHvOvPlE1NhQv/iROVq9ge9QnbDrMWC5XJ6Tk2PW08RhzzAAAAA8susWsFqtJqJt27bZc6YAAAB9EM/HgBUKhYuLi1arnTt37pYtW/z9/dlBBYU3bhQV85gNAACg91i5C3rPnj0uLi4CgUB0i0QisWI6jY2NjY2NKpVq3rx5S5Ys4Q5yUSiGDPHj/lkXFQAAoA+ysgAvW7YsMjLSZDLpb9FqtVaHEIlEa9asSUxM5Pb0GOw+JmAU98/q6QMAAPQ1VhZgoVAYGhra89kvX768oKDAaDRu2LAhKCio5xMEAADoF6wswB9//PFHH33U89mHhIQsWLBAIpFER0dHRkb2fIIAAAD9gpUnYa1evZqI1q5dy/YRCoVd3AvNvdwoPDw8PDzcugwAAAD9l5UFWK/X2zYHAADAXcVmN+JQqVS2mhQAAMCAZ2UBjo2NdXd3FwgEzJVIAoHAx8fHtskAAAAGMCt3QS9ZsuTw4cNz5syRSCRarXb16tUTJ060bTIAAIABzMotYJVKNWfOHCKSy+UqlWrdunV/+ctfbBoMAABgIOvpMWA/P7+oqKiGhoaWlhabBAIAALgbWLkLesyYMcyL+Pj4YcOGqVSq77//3napAAAABjgrC3BGRgbzQi6X19bW2i4PAADAXcGuzwMGAAAAhvUF+KGHHpJKpQKBQC6XP/300zbMBAAAMOBZWYD9/f1feeUVlUplMpnq6+sXLlw4adIk2yYDAAAYwKwswJWVlU899ZRIJCIikUi0dOnSvLw8mwYDAAAYyKw8CWvXrl0vv/zyt99+y3SuWLFi7969tktljerq6oKCAm6f8ePHKxQKvvIAAABYYGUB/v3vf09EW7duZfswlyF1/ZlINnfo0KH/t/Kv/sOGM535uTnf/7D3mcWP8RIGAADAMit3QevvwHL11ev169evFwgEbB+lUhkcHCyRSIKDg5VKpXVhWHNDHvxuVwzzN27iFLVG18MJAgAA9BK7XoYkl8tzcnK4fSIiIkJDQ7VabWhoKPfpwgAAAAObNQV48eLF7OsdO3aIRCJfX1+j0djpiGq1mrvXmohiYmLeeustIlq5cmVUVJQVYQAAAPqjbh8DfuKJJ77++mvm9aFDh/bv36/X63/88ceZM2cmJCR0d2rl5eVOTk5EJJVKKysruYNuFJeUlJV3d4IAAAD9QrcL8C+//OLr68u8fuGFF3Jzc4lo4cKFS5cutWL2QuEdN8Gljo6uCrkV0wQAAOj7ul2A9Xq9Wq2WSqWxsbGTJ08ePHgwEYlEIuaa4O7y9fVVqVRyuVytVnt7e3MHeXt5ent5cvv8eumKFbMAAADog7p9DHjUqFH/+9//tFrt4sWLIyMjmZ6lpaULFiywYvZhYWG7d+8moo0bNy5cuNCKKQAAAPRH3S7AKSkp69evd3d337x5M7vN+txzzx04cMCK2UdEROzYsUMqlR4/fjwiIsKKKQAAAPRH3d5vLJVKy8vNz42Ki4vr+hRMJhP72tPTs1vjAgAAdEqv1/t5unD7fP6f/7755xV85ekQHkcIAAAD0PRZ915IvsH8Pfr4kvomNd+JzFl5K0oAAIC+TCAQsBfacO/A2HdgCxgAAIAHKMAAAAA8QAEGAADgAQowAAAAD1CAAQAAeIACDAAAwAMUYAAAAB6gAAMAAPAABRgAAIAHKMAAAAA8QAEGAADgAQowAAAAD3h+GIPZDbK5TyoEAAAYwPh/GhKKLgAA3IWwCxoAAIAHPG8BKxQKFxcXrVY7d+7cLVu2+Pv7s4NKy8vLK6p4zAYAANB7eN4CbmxsbGxsVKlU8+bNW7JkidlQgeC2PwAAgAGD/2PARCQSidasWfPhhx9yew7x9R3i68vtczUx2b65AAAAegvPW8DLly8vKCgwGo0bNmwICgriNwwAAIDd8FyAQ0JCFixYIJFIoqOjIyMj+Q0DAABgNzwX4PDw8JycHL1e/+uvvw4fPty2E1/91p/cOB5/YrFOb7TtLHrbZ5995na7hOR0vkMBAHRiwsSJ3B+u0AWPavUGfiP9sOVrbqSZs2artXp+I/WJY8C9pLW15Ycfj7q4DiKiyxfOxfy8T6vTi0USvnN1g1qt/t2iZ1969f+Yzj8882h1XTO/kQAAOtVQ37D5h589vX2JKDnh8q6t32i0BonIgcdI/7+984+Lolr/+IFl2V2WZV1dV4QVESUjxJ+VokReLdNKzdR7yWtm6rWM6zUr09TUzIwi8hIZ1i0vqddQMzNDv6UZkSniT0BERGwFXH6jCMuyO7uc7x9Hx3FnZ3Zm2F/ief/Ba2f4PHOec84z55mdc3aGMJuTUr+67/5oAMCVy5feffv11jZC6u/JJNiZEzAAIDAwSKEIAgDIAgI87YtA/P0lqAoAAJGvJ8MXg8FguBOoIIdfuad9uYlcHohckgcGetoXADx+CxqDwWAwmHuTTv4NmAUI4Z49e6h7evfuPWzYMHLTaDQeOHCAKujfv390dLSb/PMQ1dXVR48epe4ZPnx4aGiop/yxy2+//dbQ0EBuBgQEjB8/3oP+YNzGsWPHqqqqyE0/P79Jkya5tMTz589fuHCBumf8+PEBd+0dNcTp06d1Oh11zzPPPOPry/h9rL6+Picnh7rHZDJJJBJyU6FQPP744852s/Nz7yZgq9U6bdq0seOeRJv6q5X33f/Azm+2im/NUjQ2Nv797zPjHh2DNnWXL40eO/6Lzzb4dOpngpw8efLllxcMGvoQ2iw4e3rFmvf+9fKLnvXKhuUrVpqJ9i4qFQCgzWi8XHaxqLi0i0Lqab8wLuf995PKK/XdNT0AAFaLNS/3iO5qjVrpwnSYmZm5/Zudffr2Q5tHcg5nHzk5fOgDrivRDXz66cbcvJOh2ptPHjx88MCVq/XaYBWTvqioaN4/5g97aATaPF9U4OcnDg4OCVIqAQAGQ0t1lf7M2UJloITpCBi73LsJGAAgEonWf/wF+rxvz46zp47bvBiiS5cupCDjP2mthntiAdQDMYPJWr/12ksWT69dtAOE8//5xuBhwwEAVfrKl1+YarHeZevbMcKAAM6c88qjY54AALQaWp78yzCL63/a8NiESXNvLYSc/PhwwgvPCP5M/dusSVOfQ59HDQ4nrA4q1S+yPzksrFv1xtlTxxNfWx4VPQgAoPvz0psL51rb8TnIGzwHjMFgMBiMB8AJGIPBYDAYD3AP3YJuqK+dPGmiyPfmDC6ELn8T8YkTJ1a+vQpQinnjzTcfHzuGxWTa9OnNN5rJTbPZ3Oe+GCe6VFpaunDhv6g1n/ePl6ZPm+LEImwgCGLipEmw/XaJj4974vXXXmWZSn/vvfdycn4nN/39/b/bs0fs1F8QPjt1qqHl9oTCQw8PX/vOGl9frrP7NTU1L7wwm9qM8sBAQ0sLuUkQhFgspprIZAFGYyu52SM4ePPmzX4ixivg/fv3p36SRg2epA+Thwy6HQzbt2//+ustVJMv/vNl7zAtxyo4hdkvvlilv70k6v6oqI8//ljE3Izbtm3bunUbdc+XX23upQ1h0uv1+jlz5lLbufHaNXaXFi9efP58Mbkp8vOzWu542ILNHqlM2mZsowps+s5kMt0/8CGWElNTU/fvv2O15nd7vpcHuHBFwr59+z7d+Bk1NswE4U/xWS4PbDG0kN1gtVqt7e1UQYuhNbQP2zT26tVrcnNzyU1jm5HdpbY24/Spz/hRut5yZ7Nfv944ZfJEamyYzGaJ/+2nMsQ9Er9ixVu+nXqFDZ17KAG3GY0+IsmTU/6KNpPeWQaAazNwbW2tvqpm3iuvoc2vv9x4tqiMPQEfOnRo2aoP0K+WiwrP/rz/e+cm4OvXr1+4eHHx0nfQ5nc7tp7MP+/SBNze3v7LL798lLYZbR47kv1H7qlF1naWhHrq9JnQ8P5oIRhBECveWFB/3dhT7czf7R06eHDFuylSqQwAcC7/9JGjx9vMlgCp2KEhorW19dTp0yvfTUGbP2V9X3S+ZNSjYwYNeQgAQJjNK954JbRX2KIlq5Bg1zcZpZfOTZr6XJ++kQCAhvq6rzb9+3pLG8vqoYqKitY2Ytpzs9FmavK7JWWV1ARcWlrqIw6YMPFZtLnu7df/rKx1cwLOzv5t1ryF3dTdAQB/lpVmHzpgMJqD5IwrcUpLS0WSwCeeegZtrl3x2p8VdSwJuLW19ezZs2+9k4w2D/ywu6m5gt2lP/44OmrMk+F9+gIA6mtrNqV9qO3Ve/b8f6H/fpm+oabq6oJFy7p2UwMALl+6+N2OLX363jc1YRYSbPhgTdXVivdSNqEcnH/6RPYvB9gTcGHhOZVGGxs3Gm2+8c8Xqxtu9HVlAtbpdG3m9mf/9jza/DhpddXVyvc3fO7n5wcAOHsqL+fXn++Pjhk3YTISrHlrkamt7f0Nn6PNnF9/1pWfZi/ixMmTvSMHRMcMBgAYW1vfffu1B6IHseitVuv1phuz5iaizS8+TbGZEjabTFboO/HZv6PNlPdXVV2t+CD1S5FIBAA4fSL396PHzWarVHIPpSRwTyVgAIA2rPfIR27mP6nMHT8k6NZNTZaYtXcXF5OHYx9RBCkBALAd/rz/e6e7FBSkJF06+vuvTj8+HV8fX7LE2pqq84WO32p1X9QAZGI2mVzk1fDYeHmgAgBAEERpyXm+5jKZjKzU+XP5ZaUl/W/53NZmBAAoFEGk4Mhvh/QV5QMGDUUZWl9Z/tWmfzssIrhnCHmEzZtS6YKw3n1ux7NUxrcKTmHoQyNCtb0BAPJARfahAw71vag+yxz7LJUFkPpz+acvX77o0GTgoGEDBg0FAFRc+RMAoO6uIY+wZ+e2mqqrwx6K7RnaCwAQIA/8bseWniFaUvDlZx9XARA7arS/RAIAMBqN2b84rlTfyP7kEXxF7nhaTkhoL7LELz5NAQCMGDXa398fANBqMOT8+nPv3n1Jgb+/xGKxkJuV5bpz+Q4SMAAgKnogMmm+0cTFpe7de5BF7Pomo6b6qo0gmNLOm9KSAQCxcX9BFw2GlpYqvYNLq04JngPGYDAYDMYD3FvfgNmxWIiqKj15a7SmpsZGYDaZ9Ho9OXlpsVjQ5RuJ1WoVUa5/r1+/bnMEQ0uzXq9n0nOhoaGe5QhWq9XX15c6vWojqK+vtzmg0dhKPSDd55ZmBz7TfaBums1mmwMSBFGl1/vdame6zzazRwCAmuoqaL79NLv2O+9uQQirq6vMrbe/TrG7RMdqtVZVVckot7/Yj0CPDb7c9NnA6HMLZUYZcf36NWpHGI2203IN9XUdiQ2+PYuqQd1qb2+vqqpqCbg9sWdzjrS13THbCgCoZ/W5trYWOKK6uqrdRIkNV6/soPlMEISNoLamWia6HcMdb2ebPQYX/B6ypqZa4nP7VLU6+lWS07FYLFVVesmtJzPTB6JOCU7At7l44fyAAdHyW48tra2tQb/3J8nL/T06eoBUKgUAQADr6+t9fX27de2G/tvcfKNniLaxoR7dCLK2t1utlphBw6hH+PzTj9M+fl/s5wcAMBOEXC5vqK8LClKi/zY2NkqkbL9khxDOmPZUjx7BaNNoNIaEhlZWVlB99vX1Vau7o80WQ4tWG1ZdpSd9bmxovP+BAdRj7tuzc9vmTaTP7e3tMQPveDFz+icfffLx+34iEZPP/v7+AfIAXx9fAIDJZOqmVldV6RWBCiSor6+zGU1KigsHDBhAPkuI7nNYWPjIv9xR64eGRHfrdrudQ0J7UQ9oMrU9ODi6S5ebjxG4fv2aqms3giBInwMDA+vraqk+i/3vmO6trNANjHmA6rPVaiXbudXYGhKq1VdWUn228YEvpra2Bwfd4XOXLiqL1Ur6rAhUPBT7CNVk8T/nrVIoUDu3tbWpu2vGjHua2krTn5mguRWxdn1miY122N5844bFaiXj+caNph7BIU1N19HiHYvV6uvrc6Op6Q6fVV2pHl5rrB8y8AGynRsaG0S+ImUXpQ/wQT531/QY88REqs/TJo+j+hyq7XW1ooLqc6+wcJZmbLdaHx4yoGvXrqTPPUNcOwsOYfuzTz9G9blXr97avtEUAXxkxFCynZtbmrXasNqaavTcqHbYbjAYCDNB9blHcM+mpiaynUUiUdP16126dEGCa9euoeddiHx9AQBmszlIqYyNY1tKwr9SMO7hIWq1mvQ5LKyPE4/PBd2fl2JiogPlN5d61NXVBt56Bn4nxsMJuK6ubtq0aceOHYuNjf3222+7d+/uQWd8fX3nJ76R8Pw8tDl2RJSNQCQSLVm5ftyTkwEAVqtl1OCI+/o/kLFjP/rvx0mr8479vn7DF8MeigUA1NZUzXx2nM1Ka19f300Z34ZHRAIAiovyl7360rgnn1mx9iP03wWzp5UUn2N3UiwW7zt8Cn3+Yfc3O/63+aV/LvnbzLloz5jh/eWBQft+OYE2//vFJ7/8lLV0VdJj4ycCAAiCePTBfra19vFN+vd/hjw4AgBQXXX1hb9OsPkG4ePruyljd+8+fQEA58+dXf7ay+OffvatNR+i/770wtSLxed2/JATqFAAAH7PPpj20bqEmXNf/tdSJJj6ZFx11R2zQb6+vi/9682/zrj5dK2/PHxfkFK19+BxtLl5U+rhg1k2Tt7/wIDN3/yIPievW3Eq76iNIDZu9Ief3Fzn9dbi+UWFZ77YsqdX7z4AgHMFZ1YuWTBh4tRlqz9AgvnPT7l4wfatjs89/4+XFi5Bn5+dMKquppps5z27tu3O3LJg0bJpz72A9jz6UCToMCMfGfNB6pfo89JF/zh/7sx/tu3V9uoNACg8e2rVsn/a6H2Az66sIwEBcgDAb7/838Z/v28jkEilpM/f7dj63c6tiYuXk0t14of1U3fXfPd/N5vuPxtTfjv804q1H41+bAIAwGhsHTcqZkDM4C+23lx2kLR22ekTxz5K+2/M4GEAgMqKK/+YOTnu0cfe33DzaQxL/jW3+JztdP7Tz/x1ycr16PPcv0+6eKHo2/1/oPnpXw/t35T6oY1eKpORPn/7zdff796e+NqKZ/86E+2JGxoBHa2UHDBoyOdff4c+v79m6ZlTuez6jhMQICd93vVNxt5vt9sItL1678q6uYx/U9qHv/968O33Njwy+nEAQEtz81NjhsYMGrrp691I8N7qJWdPHf/4sy1oxVO57vLLs6fFj3n8vY82IcHribOLi/I3f/NjcM9QAMCZk7nvvv260ysV1jt8x77f0Of01A+O5BxyehHs+ADwwrx/zv7HQrT55OihZrOr1n94Dx6eA169evW4cePMZvO4cePeeecdzzqDwWAwGIzb8PA34H379pWUlAAAXn/99cjIyE8//dSz/mAwGAwG4x588vPzBw4c6Kni/fz8yBU3/v7+1AU7NbV1dXeuGPrj+ImHhgxmOtSZM2d+P3IU/c4SAHDhfKHZZIoaMAj9nu/6tcYqfaUPAEG3ZrBqq/UWi+XB4aPQZl1tTfON63K5okfPm79KPH0yV+TrO2jow2iz6mpFW5sxSKlCv3psb28/fSI3ICDggZibLl3RlRFmQtMjOEjZBQBgMpkuFp+TymSR/W/+4L2s9AJBEL3D+6Kf+Rpamiuu6CQyaZ+I2z63GgyaHj19Rb4AgDZjq9FoVHZRoduSAIDC/FOmNtODw0fe8rm6+UaTPFDRI/iWzyeOifz80G9dAAD6qxVtRmMXlaprt5s+nzmZKwuQPzDg5k/6rvxZRhDmHsEh6IdPpra20pLzEqmU9PnSxQsWwtw7op9MFgAAaGlurqzQSaXScNLnogKTqS164FC01uZaY0N9XY0sQH7b57OnTCaKzzXVzc035IGBjD5Xljc21AMfIBb7AwAghC3NNwLkgRSfLxEEQfHZWFpSfKfPxQRh7hNxH/qVS0vzjcqKK1Sfi4sKTG1tAwYP9RPZ97ngzEmCMA97+KbPtTVVdbXV7dZ2/1uvf2m+0eTv7z/wls9XK8ubbzSJxWL03tP29vaaqqsBAfKoWz7rLl9qNbTIAuQSqRQAYCGIxsb6QHlgv1s+l5YUWwhzn763fb5aeUUikYVH3JwyKD6XbzK1DRg8jOpzQIA89JbP+WdOWAiC6nNLc3NgoEIT3BPtOZV3VCz2HzjkQdJnU1ubqmtXVVc1AMBqteafPiHyE3XX3Jz5vt7YIPLzC9GGofentrUZyy5ekEil/e6LIn0mCHNEv/vQHebm5hv6ynKpVNq7z22fW1sNPXqGotfsGFsNJpNJ2UUVqg0jfbZaLEMfir3pc3VVi6E5MFCh6XHbZ39//5jBt3yuuGIytam6qlVduwEALFZL4ZlTMpns/uiBZDsThLlniBZNH7YZjWWXLkgkVJ/PE2Zz38j+EuTzjaaKch0AgJzMrquptlotg4Y+jBYuNDbUNzbUBQTIQ0ifT5+wWm/7XFOtN7S0KBRB3W+tGDiVd9TfX4Lu2wMAKiuumKk+Wyzn8k9JZbL7H7jp85+XSy0E0TOkF5rEMRpbL1+6KJVK+0beT/psNpv6RUah4Gm+0aS/WiGVytCsEADg/LmzbUbj4GHDUTs3NtQ1NjQEyOXkMoX803nW9vahD464w+egILKvT+YdlUgk5IIV5HPXbt1Rs1gIy7nC01Kp7P4Hbv4M/c+yUoIwh2rD0A/5jK2tZaUXgA9A4wwAoKGu1sfHJ/L+aDTzfaPperW+UioLCAuPuOlz4VmjsXXIgyOQzw31ddca6+XywJ63fD57Og+2tw8hfa7St7a2BCqU5Lqck8f/kEpl6PdmAICKch1hNpE+EwRRVHhGJpX1v+3zRYIgKD4brlaWv7zgFZnk9nKQE2fOvvTiLOAuCgoKPJyAqUnXJgFfqaispDxkBwBQXHLR/WvzMBgMBnMvoFDIZ0yb6rbiCgoKQH5+PvQcYWFhzc3NEEKj0ajVagUcIe/U6VNnC7jrr11vyty9h1cRu3/Iqq2r464vPF985Nhx7nqTybR52ze8XDpw8BddeQV3/aXLfx789TdeRXyRsdVqtXLXZx/5o7iklLteX1W9d///8XJp245vm1tauOuPnzx9Op9XbFzP3P09L5d2//BjbV09d31h0fkjuXnc9W0m0395xsb+g79c8bbY+P2P4os8YuNqVdUP+3/i5dLWHbtaWgzc9Xxjo/Ha9R3f8YyNvT/W1vOIjYKi83/wio22tv/+L5OXS/t/PnSlopK7vvTyn4d4x8YWq7Wdu/7X3/+4wCs29FU/HOAZG5m7Wgw8YsNt5Ofne3gR1sSJE7dv3w4ASE5Onjx5smedwWAwGAzGbXh+FfTWrVulUunPP/9coE5YAAAfqElEQVS8evVqzzqDwWAwGIzb8PAq6O7du//++++OdRgMBoPBdC7ws6AxGAwGg/EAogULFvTo0cOx0FshCEugPEAZxPWhZRBCi9US0jOYexFtpjZNdw311ZXsWCwWqVTSVdWFu0sms6lXaCh3l0wmc7euKhmHl8kgrFarn59f91tPc+SC0WgM66VleWuvDWazWakMCpTLHUsBAAC0t7f7AJ8eGh7PPjMa20JDevpxfno2YbEEBvCIjXYIrbxjw6Tp3p17bBAWq1TCIzYAhCazuVco4wv76JhMJr6xIfbzU/OJjVajsTfP2OiiVPKKDeAD+MdGMPcnqxMWnuNGO7RYrXxjo4emuz+vcYNXbABgMvGMDbO5W9euMhnXVyVarRY/L4sNa3u7D9/YaDOG9uzJ96n7bqCmpsbDP0PCYDAYDOYepKCgAN+CxmAwGAzGA+AEjMFgMBiMB8AJGIPBYDAYD4ATMAaDwWAwHgAnYAwGg8FgPMDdmoA/+OCDN998s6qqyrFUqElBQUHXrl1fffVVjvpLly517dr1lVde4e7StWvXXn31Ve4vYeTrEl+9AJf4tqqAjuNbC75VEGDi6lgS4JKrqwBcH34COs4LO6ITnBFucMkLO84j3K0JeOnSpU1NTSEhIc8995yLTAYOHFheXm4wGEaNGsVF369fv/LycqvV+sgjj3DRf/LJJ127do2NjT127BhHE74u8dULcIlvqwroOF61EFAFN9Ta1R3hhioAF4efgCoA7+sIAS554Rnhhtjwwo7zDJ59G1JHmDFjxujRo11tAiFUKpV6vZ67XqPR6HQ6dk1ycrJGo6EWYeDzvg6+LnHRC3aJb6sK6wXIoRYCquC2WpPHd3pHuLkK0AXh15HTwXs6QrBLXnVGuNqlDhbh0o5zM/n5+XdrAnZb9oUQymSy+vr6jRs32v1v/a03ji1cuHDGjBl6vV6pVLIn4KKiIplMRm42NTXJ5XIIIVMRTC5xFHPRM7nkkI6PNc6qtYAquK3WJE7vCCdWwdXhx3R8wVWAnugIh63ktuwLhTasgCo4PTa85wzyIHdrAu549s3Pz1epVIsWLbKRrVmzZtiwYfHx8WlpaUePHk1ISFAoFEuXLl2zZo1CoYiOjrbRl5WVxcTEoM8EQcjl8ri4uJSUFAhhY2PjokWL0tLS6M6Eh4dTM7RWq922bRuEMDExkV4Ek0tMx2fSs7cPk0vs2LQqS5Xt6hG8as23CkwdzWLy008/RUVFMZnQa2E0GvPy8oqKirhXgclEQC2cUgXkrd0Id2L42e1opipACEtLS1Uq1YIFCzjWgknv3DOCqRZ2XXIIXZ+SkqLVamfPns2xFkwdx1QFFj2TS3xjg2/4uaHjmFrVs9yVCZgpxHU6XWpqKneT5ubmefPmjRw5krozKSlJLpdXVlaWlZUVFxeXlpY2NzevWbMmJCQEQrho0SKbKDSZTAAA9NlqtZKfU1NTAQCZmZkzZsyIi4uzKVqlUpGfIyMjqSFFP73tusRyfLt6hw3F4hJTw9q0KnuV6XoqHGstrAp2O5rJJDU1VS6XFxYWzps3z663NrVIT08HAGRlZT3xxBMcO4LFREAtOl4FCCFLhDs3/OxmL5bYa25unj9/PvdwsqsXEEvsXjHlYL5DE13f3Nwsl8vLy8tnzZr18MMPO6wFS8fZrQK73q5LAmKDb/hBQR0HOY8DLK3qWe6+BLxnzx5q51VWViYlJUVERKjVapVKBQCg352wMbGBPqOQlJSkVqupe0aOHLlu3Tr0mX7upaSkSCSSkSNHqlSqNWvWQA4zEOnp6RKJJC4uDgCwYcMGG5fmzJlDD3SqSw6PT6+Cw4ayccmh3qZVHbrE3gtcas23CjbHtzt1RDdRqVTkYdVqtclkYqnF2rVr5XJ5dXU12hwxYsTJkydZqsDFhG8tOlgFBHuEdzz8qNA7mr3K0N6iCvZwouv5xpJDr+i14Ds00aug0+lyc3PJtg0JCWGvBXTUcfQqsOs7HhtQUPiROOw4yH8ccNiqHuTuS8BUdu/eDQA4c+ZMY2NjdnY2AKCkpITvQezOKCQlJQUHB0PK/G50dDRKrhDC7du32+jLy8tzc3NLS0sh5xkInU6Xl5dnc0GXn5/fv39/lUpFRjzdJY7HJ/WQc0ORLvFt2A5OunCpNd8q0P/FNHVEmjQ1NUEINRpNbm4uhNBkMimVSha3S0pKZDLZxo0bNRrN4sWLIYS5ubk5OTlMVeBuwrcWgqsAOUd4R8KPhKWjqVXmu6iCo55vLEH+JymJgKEpJSVFLpdPnz5drVbPnj3bYS04dhxZBY56Knxjg2/48e04yH8c4NiqnuLuTsAQQnQHjN4TtbW1w4YNsxHzmlHIyckpKyuLiopCm83NzWKxmItLAiZT9Xp9QkKCRCKZOHEiaUuvAhqpWY5vY0Id2e02lN1WYtE7scqQodZ0yFpwd0nA1FFZWdmgQYMghHl5eWKxOCYmRq1WZ2ZmsphERkaSnwEALMssySpwNxFQCwFV4BXhDsPPrh5y7mjSJaZFFRBCm69TfPVcYolehIBasBdhF5lMhjK9yWRSqVQxMTHJycl2lQKGJhZ9bW3tkCFDOmiCXGIKP7tFsHecs4YyplZlGfrcyV2fgCGEI0eOpGdfAAA9KB3OKPz000/UTer8LkEQIpHI5oA2egTL1BHdJC8vT6PRREZGomtGh1VgOT6LCcKmofjqSYqLizm6xGTCVGuWIni55LCj6SZNTU3UptBqtTa1oLuk0WgIgkCfAQDkZ5Yq8DLhG64Oq0A3ERDhTglvji5RF1UYDAaFQgEAeOKJJzqiJ6HHEpMJSy10Ot3SpUt3797NsQgWvVwuR98gCYKQSCTsJiwdx0uPBgFqnwo2YQo/Jj1Tx5Emjz32GMrodOwOZY899hg9zdttVYdDn9u46xMwug6aOHEiOUmDGjclJWXlypV0vd3ZqcbGxjlz5qDXNdssTKXO765atcqhHjJMHbGY0L8GsVfB7vHZTegNxVdvs5/X5KtdE5Yvf3b1fF1in4a0a7J+/XqRSBQfHy8SiT7//HOH+s2bN8vl8u3bt6vVaptmZKoCXxO+4cpUBSdGeMfDm5dL5J3PqVOnpqenQwjnzZs3c+bMjughQyyxmNBrYTQaNRpNfHz8mTNnJk6cSF/aY1OEQ31aWppEIpk1axZZC3YTesfx1aNBICQkZNasWdAefE3o4ceut9txyGTnzp0QwoSEBPoAa3coQ/qFCxfa5Gx6qzoc+tzJXZ+A165dS//uu3PnzsjISJuvFyTUGYXi4uLIyEiVSvXll1+ilXJ0vU6n27JlCyqFix7eOXXE0YRXFWympriYUBuKl95oNJI7OU6+cjQh4ajn6xK1ozmaNDY2lpaWEgTBUV9SUjJy5Mji4mLuVeZrwjdcySpwN+Eb4R0Jb44m1EUViM8//3zJkiXoc//+/Tuotxk3uJjYIJFIqLf3Q0JCbC6ebIpwqIcQ6nQ6qpVDE2rH8dWTg4BarUZ31FNTU+nrovmaUMOPi96m46jZFEJYWFh45MgRG5foQxn1N8p2Z8FJEy5Dnzu56xMwFbJxS0pKEhIS0E6r1Yrm0qjKnJyctLQ0lUrVv3//8PBwtHP58uXkVRgdvnphJtyrINiEl54giIiICPSZ42wWXxOX6tHUkVe5JKwWbgg/7zwjDAYDyiL19fXkQtY5c+Y4Sy/MJD09nbxbgAgPD2e5qcNX7+oiyEGguroaLalDvytj8YevSUeKIPcMGTKE5bxA+uTkZAAA06SV3eNzH11dTedJwAaDgew8rVbb2NhoMBgWLFig0WhGjBhBb9/Dhw+jS/jZs2fHx8dDCCUSCfVLSQf1Akz4VkGACV89QRBisdhoNO7du5dMEuTvAu1CN3G13g0usRfhBpfcEH5eeEZACHU63b59+9DnsLCw2tpaFrEAvTCT8PBw6lqt8vJylr4ToHdpEdRBYN26dfHx8Q5TI1+TDhaBSElJCQsL46I/cuSI3RkfJj3H0dUNdJ4EDCFEswW5ublRUVFTpkyRyWQ7d+5MTEx02LgzZ84MDw9HIwIX+Oq5m7BUwWq18jVxShEbNmwQi8VarRatZWDPE3QTV+vd4BKXItzgEonrws9teu4mBoNBIpGgu4VDhgyh3qt0il6YCRrB0Wej0QgAOHr0KEst+OpdXQQ5sRoSEpKYmIhSI0EQLM9Y5msioIg1a9ZoNBqUGhcuXEiu22LqCOr0cGVlJbsYChpdXU2nSsCI4OBgAAD6iR5qXEBbbkonLCysvLwcfeYyGvLVU00c6ulVgPYWzbKb8NU7LIKL527WO7EItPrGKSbO0rOYuDT8hBXhOpfQPcawsDA0Im/YsAEAEB4eTn0YSEf0Aky2bNkil8tzcnJWrlwpkUj27NmD9jN9m+erZzLhq2c3aWpqAgCg1Lh+/Xq0Wopl6aIAE776jIyM8PDw8PBwNDHBpe9IOIqFDX0uohMm4KysLHQ5Qzbuxo0bAQAs1zh6vZ48/9FTT8PDw8eMGeMsPdWEi55eBYe14FtrAUWgGRTqf6Ojo19//XWmWrha78QiWBIAXxNn6SFzWrIJPy6pjhp+vPQcTVztUlNTE/pimpmZiQb0/Pz85ORku48XFaAXYFJWVnbkyBHyS1hKSopYLI6MjCSntzuotzHhq+dicvToUZQaMzMzlUolykDr169/6qmnmIrgayKgCBLufccipl/CChj6XEcnTMCIxMRErVYbHBw8efJkCGFqair5o3I6GRkZ6IKROhasXbvW7u/TBehJE+56eCs+UlJSONYC8qw13yLq6+up14kOU5dT9JB1gHa1S95Za7vhxw49/LjouRfhBpcQwcHB5eXlaNladnY2SzYSphdmsm/fPo1Gg4bvtLQ0cuaS6QaGs/TOKkKtVpN3houLix2uABdgIqAIXh1hV8wSXQJGV1fQaRPwpk2b0BN316xZAwDQ6XTU37bbBSnJeZTS0lJynapH9BkZGehHGtxrwbfWfItAj4YYMmSIRqNBeQV9m2eayeugHlJuGLioCOopmpSUtGTJEvocFZMJXz2Tid1asxcB76obDE50Sa1Wo0k+9NWK/TlfAvTCTMLCwqh3ehUKRUhICMvo33E9QRBOLEKhUKC1CxBCtVp94MABxqoKNRFQBK+OoIvZr+0EjK6uoNMm4NraWrFYjM7tgwcPAgDQz66ZegXtnzBhAjmHHxwczHKF7iw9i0tMtdi7dy/T08z56oWZ0L/VpaWlsVyfCtPDO1vGFUXQW37+/PkAAPInCg5N+OpZTJi++zLp7X51NhqN5ERsB/VuKEKASxkZGRKJJDc3V6fToXU3DsdZG70AE4df08PCwsgLawhhaWnpU089BZgX/XZcDyF0YhGpqakSiWTEiBEymWz58uVoZ3Z2NsvyVbqJc/WQoe+YprRtxFxm+gQMfU6n0yZgCGFKSopMJouJiaF+sRCLxaNHj7Y5nYqLi9Ge0tJSmUwWFxcnk8lWrlzpaj2LSyy1UKlU1FOrg3oBJtnZ2TZDUm1tbUZGBmT4xsait2uSnZ0NaaOe4CI46hEsL0y0a8JXz2Jit9bsRdh8dUYriUJCQhQKhVP0bihCgEs5OTmRkZFnzpyB3FZUUPUCTLjo9+3bJ5PJdDoddQ18amrqzp077YZfB/WuKEKn0x09epS6MyQkhEx7drExcboe3tkRDqe0STH3mT4Bo6Vz6cwJGGHzxQL9DLG2tpbp5l5ZWRmKEhs9ZBjKBevpLjGZUGtx4MCB6dOnk/uZVg3w1fM1sXkYZGRkZGFhIfps9xsbi16AiSv0kMOr1G1M+OpdUQS81XGZmZkqlQp11pw5c1ieS8BX74YiBLgE+azAEGzCXb93796IiAj0unsu9zwE66G9qzSnFEGlrKyMy+S32/Qss+A2sMz0OWt0dSKdPwEzhSxkjUKmm05MJnz1fE3IF86o1Wp0EyY5OVmhUNh9UbkAvTAThM28ncOcQZ/n42vidD1d89NPP0VFRS1atMhZetcVgb46q1QqcmTR6XTkFT0dvno3FCHAJaZxlmXWnK+JgCKMRiP9yZos4cdX754iIITh4eHoe+fmzZtVKlVcXBxLrZ2ih6wNa3cW3K5+w4YNdmf6EE4ZXZ1I50/ACLtv+WaJQrt6FhO+er4m6Fvy4cOHZ86cOWfOHADAggUL0E67UciiF2DCcmJ0yuybmpoql8sLCwvnzZtn15av3g1FUN8TTLYAS8fZ1QswcbXergnLigrIMMjyNRFQBISwtraW+sZJ6Cj8+OrdU4Rer0dXPyKRiDpuMNXaWXoWE7uz4Ex6+kwfe92FDX1O4V5JwHS4jMsdNHFWEejH7BkZGUqlUqlUUp88jrCJQod6ASZMJwb67sK9vlS9ABNX6Pfs2WOjUalUZCZQq9U2L4jlq3dpEUVFRQqFQq/XoxfLREdH23xxtOk4h3oBJq7W25iwrKhA0Dudr4mAIkioT2LiEn589W4oYuPGjXYHASZbZ+lZTOiz4Ox66kwfu1jw0OcU7tEETO8Jp99ydO4tyrKyslWrVlFf9sJeHXa9ABOH523Hm9ShScf1Dk3Q6a3RaNCbX00mk1KpZPJfgN4VRezcuRMAUFpaarVaw8LCHN5gYNcLMHG13q4Jgj7OOgxUviYCimCSOT1cXX0GOXTPiXqHJtRZcAFFOHF0dSL3YgKmN6jT7we64RYlS3Uc4vRzif6NzaH/fE06rndoUlZWhl4mmpeXJxaLY2Ji1Gp1Zmam0WjMy8ujv5eUSQ8h5GvSQX1WVpZMJgMAkL8hQTB1HJNegImr9SwmdLznwtoN4erqM0hArZn0Akycq3fn6MqLey4B2w10595ydMMtShJvC3S+/nfExOlFNDU1icViclOr1S5dujQ9PR0AkJWV9cQTT9gsyrCrhxDyNXGW3mbRpsPYoC/ydNjX7EXw1TvFJZaDe8OFNYkXnhHCBhm+rSTAxLl6d46ufLnnErANrr7l6NJblN4W6G6osquLWL9+vUgkio+PF4lEn3/++dq1a9GzctB/R4wYcfLkSRY9hJCvidP1CC+MDZe65J0X1ggvPCO46zveSgJMXNQR0MWjqwDu6QTMcgvRI3peJt4Z6N5zV1awSWNjY2lpKUEQJSUlMpls48aNGo1m8eLFEMLc3NycnBybg5N6CCFfExfpvTA23OASFe9JYF54RghwSVgrCTBxqd6lo6sw7ukEzHQLkSkKnaV3YhFUQ+gFge5td2UFm0AIqT/eAAAYDAb0ubGxcdGiRWlpaRxNXK1nN4FeExtuK8KrEpgXnhECXBLQSt7WESwVd/royp17OgFDe7cQ2aOw43qnFwE9F+h29d55V1aAiUajIR9TTD6yODU1FT3qfcaMGfS+oJu4Wu/QJa+KDfcU4W0JzAvPCAEuueHC1w1XEm4YXXlxrydgeOctRC7jckf0LirCI4HOovfCu7ICTDZv3iyXy7dv365Wq9FvQJOTk6nv+lYqleR3ULsmrtZzccnbYsM9RXhbAvPCM0KAS2648HXDlYSrR1de4AR8G+5DuTC9S4twc6BzXAoEvfKuLPciSkpKRo4ciR5KXFRUJJPJyH81NTXRn/BHNXG1nrtLXhgbbijCCxMY4q4+I9xw4eu2jnDd6ModnIBv41WBLkDvtkDnFeVeeFeWbxGI8PBwnU5Hbmq1WuozAdyv52XihbHhnvCDzOeps/R8TTrHGeHqVnJDEXbFTM+eFBx+7OAEfBsvDHRhqcKrLrG98K4s3yIQKpWK2gLkejomXK0XZuJVseEel+yep07U8zXpHGeE3SqzN5S3dQRTFdifPckrbTsEJ+DbeGGgC0sV3naJ7YV3ZfkWASFMT0+XSCRxcXEAAKYXabhTL8zE22LDDS7Rz1Pn6gWYdIIzgl5lh7X2to6wWwXo6OlXwtI2EzgB34EXBrqAVOGFl9gIr7orK0Cv0+ny8vKoL29hx9V6ASZeGBtuuCqlnqeu0AszgXf5GUGtMnRNw7q6I2yqADk8e1JY2mYCJ2D7eFWgC9B74SU29Mq7sgKKuNvxwthww1UpwtV6viad5oy42zsCwTGJCkjbTOAEbB8vDHRhJ4ZXXWJ74V1ZAUV0GrwqNjqHnq9Jpzkj7vaOgB1Ioh15YQNOwPbxwkAXdmJ42yW2F96VFVBE58DbYqMT6AWYdI4z4m7vCLvPnuRCB1+XhBMwI14Y6AJc8sJLbIyX4IWxcbfrhZl0Au7NjhCctkny8/N98vPzBw4cCDCdlCtXrtTW1kZFRQUGBrpCL8wE4w14YWzc7XphJp0A3BECKCgowAkYg8FgMBh3U1BQ4OtpHzAYDAaDuRfBCRiDwWAwGA+AEzAGg8FgMB4AJ2AMBoPBYDwATsAYDAaDwXgAnIAxGAwGg/EAOAFjMBgMBuMBcALGYDAYDMYD4ASMwWAwGIwHwAkYcxfw448/Dhw40N/ff8CAAfv37yf3+/j4eMolm6J97AEAGDx4sCuK4/Vf55ZFpaWl5Y033rBr4sGu6QhvvPFGS0uLp73A3CvgBIzxds6ePTt37tz09HSz2fzVV1/NnTv3xIkTnnbKFvIB6zafz54962nXXEhiYuIrr7ziaS+cySuvvJKYmOhpLzD3CjgBY7yddevWffjhh6NGjQIADB8+PCkp6YMPPiD/+/XXXwcGBsbGxtbU1KA9FRUVo0aNkkqlAwYM2LFjB9p57dq1p59+WiqVjh8//tq1a2inj4/Prl274uPje/XqRR6wT58+DQ0NdvV1dXWxsbGBgYH/+9//ODpPfhH08fH57LPPevTo0bt37/379y9btiwoKGjw4MHnz59n8dDuATdt2tSzZ8+ePXv+8MMPZBHoL99qjh071sfHx8/Pr2/fvocOHbIpy25Lkvz6668qlSoiIoK9Berq6saOHevv7z927NiGhgaqS2PHjmUqhaki33//fZcuXajdTT/+hQsXULRcvXrVx8fn6tWrAIDY2FjU1CxNNHbs2IiICKVSSW8KDMYl4NcRYrwchUJhNBrJTaPRqFAo0GcAwNKlS61Wa2pq6vz589HOmJiYvLw8CGF2dvaMGTPQzsTExC+//BJCePjw4cWLF5PmGRkZEMLRo0fn5uZCCPPy8tArxuzq58yZc+DAAQjhqlWrAOWbLhWb/eQmcpUgiKysLABAVlYWhHDv3r1RUVEsHto9zsqVKwmC2L17d3h4uM1/+VaTZM+ePZGRkTZHs9uSJNOnTz98+LDdWlP3LFiwIDk5GUKYkpKyYMECG5eYSmGqyJIlS2y6m358q9Uqk8kghOnp6SqVKj09HUIok8msVqvDJkJuTJ06FWIwLga/DxhzF0Af3MVisc2/TCYTmZWjo6PXr1+v1+upJhqNxmQyQQitVmtwcDBpXlJSAiFMTU1Fr+xevnz5xo0bmfRKpRIN4iaTSUACtqsRiUQsHrIfh7Qld/KtJhX60ey2JIlCoSAIgjShg/6lUqmQzGQyka9JJ11iKoWpIgaDAd7Z3XaPHxYW1tTUNHHixOXLl0+cOLGpqUmr1XJpIpuDYzCuAydgzF2AUqmkfgOmjo/UbERmZZPJtHbt2sjIyGHDhuXk5JBKEnqmKS8vR9//+vfvX1lZyaQnP0B7lwV29ztMwFQBvUSOx2E/CEs1S0pKEhISgoODZTIZ/Wh2W5KEbHC7rWHXYfqVE1Mp7BVhOhS5c8qUKXv37lUqlQRBKJXKvXv3TpkyheORbaqGwbiI/Px8PAeM8XaeeuqpXbt2kZs7duyYPHkyudne3g4AMJvNKpUK7fH393/77bcvXryYlJSUkJCAdpLfeyCEFovFpohevXoFBQV999133bt3Dw0NZdIHBQWh4lyxUJbdQ6cchF7NSZMmxcbGlpSUtLa20o9mtyVJpFKp2Wx26JJKpUIys9ls99XovPqrra0N3Nnddo/frVu3jIyMCRMm+Pn5TZgwISMjo1u3blyaCB1HKpU6rBcG03FwAsZ4OytWrFi5cuXx48cBAMePH1++fPlbb71F/vftt98GAHz66afTp09He55//nm0iEalUmm1WrTzb3/728qVK9vb2wsKCl588UV6KVOmTFm8eDGZ2u3qExISvv/+ewDAunXrnF5Nhx6y0L9/f3RlwLea1dXVU6ZMAQAsW7aMLrbbkiTjx4/Pzs526FtCQgJaNPfee+/RszhTKUwVeffdd8Gd3W33+PHx8T/++OPTTz8NAJg0adKPP/4YHx/PfmSSY8eOjRs3zmG9MBgngG9BY7yfw4cPDxo0SCwWx8TEkAt/IIQAgG3btslksvj4+Pr6erQzMzMzKipKJBKNGDEC3WiFEDY3N0+fPl0kEkVERGzZsoU0Jw9VXFwMANDpdCz62trakSNHymSybdu2AWffgrZbIsfjZGdnjxkzRkA1t23bJpfLw8LCNm/eHBwc3NjYSNXbbUmSgwcPUhdVMTlcX18/ZswYsVg8ZswYso+oel79tXv3brlcTu1uu8fPysoSiURos7GxUSQSoVVvXJooMTHx4MGDEINxMfn5+T75+fkDBw50b9LHYDCdgeeff3716tX9+vVzT3E+Pj6QYcGXs7h8+fLq1au3bt3q0lIwGABAQUEBvgWNwWAEkp6e/sUXX7itOIlE4uoiNm3alJ6e7upSMBgE/gaMwWAwGIy7wd+AMRgMBoPxDDgBYzAYDAbjAXACxmAwGAzGA+AEjMFgMBiMB8AJGIPBYDAYD4ATMAaDwWAwHgAnYAwGg8FgPABOwBgMBoPBeACcgDEYDAaD8QA4AWMwGAwG4wFwAsZgMBgMxgPgBIzBYDAYjAfwAwAUFBR42g0MBoPBYO4t/h9iDjA79hqibwAAAABJRU5ErkJggg=="/>
</div>
</article>
</section>
</section>
</body>
</html>





```python
#ets_results.ALL()
```

## How would we get these results in a batch python script? Set batch to True and get the HTML returned to you to write out to a file and view later


```python
sas.set_batch (True)
```


```python
q = ets_results.DECOMPOSITIONPLOT
```

### q is the Dict with the LOG and LST. The LST is the HTML of the result. We'll display it here, but if you write it to a file it will render when you open it in a web browser too.


```python
HTML(q['LST'])
```




<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="SAS 9.4" name="generator"/>
<title>SAS Output</title>
<style>
/*<![CDATA[*/
.body.c section > table, .body.c section > pre, .body.c div > table,
.body.c div > pre, .body.c article > table, .body.c article > pre,
.body.j section > table, .body.j section > pre, .body.j div > table,
.body.j div > pre, .body.j article > table, .body.j article > pre,
.body.c p.note, .body.c p.warning, .body.c p.error, .body.c p.fatal,
.body.j p.note, .body.j p.warning, .body.j p.error, .body.j p.fatal,
.body.c > table.layoutcontainer, .body.j > table.layoutcontainer { margin-left: auto; margin-right: auto }
.layoutregion.l table, .layoutregion.l pre, .layoutregion.l p.note,
.layoutregion.l p.warning, .layoutregion.l p.error, .layoutregion.l p.fatal { margin-left: 0 }
.layoutregion.c table, .layoutregion.c pre, .layoutregion.c p.note,
.layoutregion.c p.warning, .layoutregion.c p.error, .layoutregion.c p.fatal { margin-left: auto; margin-right: auto }
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r table, .layoutregion.r pre, .layoutregion.r p.note,
.layoutregion.r p.warning, .layoutregion.r p.error, .layoutregion.r p.fatal { margin-right: 0 }
article, aside, details, figcaption, figure, footer, header, hgroup, nav, section { display: block }
html{ font-size: 100% }
.body { margin: 1em; font-size: 13px; line-height: 1.231 }
sup { position: relative; vertical-align: baseline; bottom: 0.25em; font-size: 0.8em }
sub { position: relative; vertical-align: baseline; top: 0.25em; font-size: 0.8em }
ul, ol { margin: 1em 0; padding: 0 0 0 40px }
dd { margin: 0 0 0 40px }
nav ul, nav ol { list-style: none; list-style-image: none; margin: 0; padding: 0 }
img { border: 0; vertical-align: middle }
svg:not(:root) { overflow: hidden }
figure { margin: 0 }
table { border-collapse: collapse; border-spacing: 0 }
.layoutcontainer { border-collapse: separate; border-spacing: 0 }
p { margin-top: 0; text-align: left }
span { text-align: left }
table { margin-bottom: 1em }
td, th { text-align: left; padding: 3px 6px; vertical-align: top }
td[class$="fixed"], th[class$="fixed"] { white-space: pre }
section, article { padding-top: 1px; padding-bottom: 8px }
hr.pagebreak { height: 0px; border: 0; border-bottom: 1px solid #c0c0c0; margin: 1em 0 }
.stacked-value { text-align: left; display: block }
.stacked-cell > .stacked-value, td.data > td.data, th.data > td.data, th.data > th.data, td.data > th.data, th.header > th.header { border: 0 }
.stacked-cell > div.data { border-width: 0 }
.systitleandfootercontainer { white-space: nowrap; margin-bottom: 1em }
.systitleandfootercontainer > p { margin: 0 }
.systitleandfootercontainer > p > span { display: inline-block; width: 100%; white-space: normal }
.batch { display: table }
.toc { display: none }
.proc_note_group, .proc_title_group { margin-bottom: 1em }
p.proctitle { margin: 0 }
p.note, p.warning, p.error, p.fatal { display: table }
.notebanner, .warnbanner, .errorbanner, .fatalbanner,
.notecontent, .warncontent, .errorcontent, .fatalcontent { display: table-cell; padding: 0.5em }
.notebanner, .warnbanner, .errorbanner, .fatalbanner { padding-right: 0 }
.body > div > ol li { text-align: left }
.c { text-align: center }
.r { text-align: right }
.l { text-align: left }
.j { text-align: justify }
.d { text-align: right }
.b { vertical-align: bottom }
.m { vertical-align: middle }
.t { vertical-align: top }
.aftercaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    padding-top: 4pt;
}
.batch > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.batch > tbody, .batch > thead, .batch > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.batch { border: hidden; }
.batch {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: 'SAS Monospace', 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    padding: 7px;
    }
.beforecaption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.body {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    margin-left: 8px;
    margin-right: 8px;
}
.bodydate {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: right;
    vertical-align: top;
    width: 100%;
}
.bycontentfolder {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.byline {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.bylinecontainer > col, .bylinecontainer > colgroup > col, .bylinecontainer > colgroup, .bylinecontainer > tr, .bylinecontainer > * > tr, .bylinecontainer > thead, .bylinecontainer > tbody, .bylinecontainer > tfoot { border: none; }
.bylinecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.caption {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.cell, .container {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.contentfolder, .contentitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.contentproclabel, .contentprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.contents {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.contentsdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.contenttitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.continued {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    width: 100%;
}
.data, .dataemphasis {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.dataemphasisfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.dataempty {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datafixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.datastrong {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.datastrongfixed {
    background-color: #ffffff;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.date {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.document {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.errorcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.errorcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.extendedpage {
    background-color: #fafbfe;
    border-style: solid;
    border-width: 1pt;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
    text-align: center;
}
.fatalbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.fatalcontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.fatalcontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.folderaction {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.footer {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footeremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footeremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.footerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.footerstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.footerstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.frame {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.graph > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.graph > tbody, .graph > thead, .graph > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.graph { border: hidden; }
.graph {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.header {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headeremphasis {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headeremphasisfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.headerempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.headersandfooters {
    background-color: #edf2f9;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrong {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.headerstrongfixed {
    background-color: #d8dbd3;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.index {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.indexaction, .indexitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.indexprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.indextitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.layoutcontainer, .layoutregion {
    border-width: 0;
    border-spacing: 30px;
}
.linecontent {
    background-color: #fafbfe;
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.list {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.list10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.list2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.list3, .list4, .list5, .list6, .list7, .list8, .list9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: disc;
}
.listitem10 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.listitem2 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: circle;
}
.listitem3, .listitem4, .listitem5, .listitem6, .listitem7, .listitem8, .listitem9 {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: square;
}
.note {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notebanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.notecontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.notecontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.output > colgroup {
    border-left: 1px solid #c1c1c1;
    border-right: 1px solid #c1c1c1;
}
.output > tbody, .output > thead, .output > tfoot {
    border-top: 1px solid #c1c1c1;
    border-bottom: 1px solid #c1c1c1;
}
.output { border: hidden; }
.output {
    background-color: #fafbfe;
    border: 1px solid #c1c1c1;
    border-collapse: separate;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    }
.pageno {
    background-color: #fafbfe;
    border-spacing: 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    text-align: right;
    vertical-align: top;
}
.pages {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: decimal;
    margin-left: 8px;
    margin-right: 8px;
}
.pagesdate {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.pagesitem {
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    list-style-type: none;
    margin-left: 6pt;
}
.pagesproclabel, .pagesprocname {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.pagestitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: bold;
}
.paragraph {
    background-color: #fafbfe;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.parskip > col, .parskip > colgroup > col, .parskip > colgroup, .parskip > tr, .parskip > * > tr, .parskip > thead, .parskip > tbody, .parskip > tfoot { border: none; }
.parskip {
    border: none;
    border-spacing: 0;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
    }
.prepage {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    text-align: left;
}
.proctitle {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.proctitlefixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooter {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooteremphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooteremphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowfooterempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowfooterstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowfooterstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheader {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderemphasis {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderemphasisfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: italic;
    font-weight: normal;
}
.rowheaderempty {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.rowheaderstrong {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.rowheaderstrongfixed {
    background-color: #edf2f9;
    border-color: #b0b7bb;
    border-style: solid;
    border-width: 0 1px 1px 0;
    color: #112277;
    font-family: 'Courier New', Courier, monospace;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.systemfooter, .systemfooter10, .systemfooter2, .systemfooter3, .systemfooter4, .systemfooter5, .systemfooter6, .systemfooter7, .systemfooter8, .systemfooter9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.systemtitle, .systemtitle10, .systemtitle2, .systemtitle3, .systemtitle4, .systemtitle5, .systemtitle6, .systemtitle7, .systemtitle8, .systemtitle9 {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size: small;
    font-style: normal;
    font-weight: bold;
}
.systitleandfootercontainer > col, .systitleandfootercontainer > colgroup > col, .systitleandfootercontainer > colgroup, .systitleandfootercontainer > tr, .systitleandfootercontainer > * > tr, .systitleandfootercontainer > thead, .systitleandfootercontainer > tbody, .systitleandfootercontainer > tfoot { border: none; }
.systitleandfootercontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.table > col, .table > colgroup > col {
    border-left: 1px solid #c1c1c1;
    border-right: 0 solid #c1c1c1;
}
.table > tr, .table > * > tr {
    border-top: 1px solid #c1c1c1;
    border-bottom: 0 solid #c1c1c1;
}
.table { border: hidden; }
.table {
    border-color: #c1c1c1;
    border-style: solid;
    border-width: 1px 0 0 1px;
    border-collapse: collapse;
    border-spacing: 0;
    }
.titleandnotecontainer > col, .titleandnotecontainer > colgroup > col, .titleandnotecontainer > colgroup, .titleandnotecontainer > tr, .titleandnotecontainer > * > tr, .titleandnotecontainer > thead, .titleandnotecontainer > tbody, .titleandnotecontainer > tfoot { border: none; }
.titleandnotecontainer {
    background-color: #fafbfe;
    border: none;
    border-spacing: 1px;
    color: #000000;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
    width: 100%;
}
.titlesandfooters {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.usertext {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warnbanner {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: bold;
}
.warncontent {
    background-color: #fafbfe;
    color: #112277;
    font-family: Arial, 'Albany AMT', Helvetica, Helv;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
.warncontentfixed {
    background-color: #fafbfe;
    color: #112277;
    font-family: 'Courier New', Courier;
    font-size:  normal;
    font-style: normal;
    font-weight: normal;
}
/*]]>*/
</style>
</head>
<body class="l body">
<h1 class="body toc">SAS Output</h1>
<section data-name="DOCUMENT" data-sec-type="proc">
<div id="IDX" class="systitleandfootercontainer" style="border-spacing: 1px">
<p><span class="c systemtitle">&apos;</span> </p>
</div>
<div class="proc_title_group">
<p class="c proctitle">The TIMEID Procedure</p>
</div>
<h1 class="contentproclabel toc">The Timeid Procedure</h1>
<section>
<h1 class="contentfolder toc">Decomposition</h1>
<article>
<h1 class="contentitem toc">Time ID Decomposition Plot for WEEKDAY145W BEGIN</h1>
<div class="c">
<img style="height: 480px; width: 640px" alt="Time ID Decomposition Plot for WEEKDAY145W BEGIN" src="data:image/png;base64,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"/>
</div>
</article>
</section>
</section>
</body>
</html>




### the ALL() method returns a List of Dict's which is easy to traverse. Can write them out to their own files to view later. Just display them here for now.


```python
from IPython.display import display as DIS
x = ets_results.ALL()
for i in range(len(x)):
    DIS(HTML(x[i]['LST']))
```


```python
sas.set_batch (False)
```

## The following isn't needed, SAS will shutdown when you stop the notebook. But you can shut it down manually if you want


```python
sas._endsas() 
```

    SAS Connection terminated. Subprocess id was 4556



```python

```
