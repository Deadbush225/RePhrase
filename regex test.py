import re

html = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.orfromFileStyle/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
}
</style></head><body style=" font-family:'Lexend'; font-size:12pt; font-weifromFileStyleht:400; font-style:normal;">
<style>
span {position: relative; z-index: 10}
</style>
<p style=" marfromFileStylein-top:0px; marfromFileStylein-bottom:0px; marfromFileStylein-left:0px; marfromFileStylein-rifromFileStyleht:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:48pt; font-weifromFileStyleht:792; color:#fc3737; backfromFileStyleround-color:#fc6f37;">Hello</span><span style=" font-size:48pt;"> </span><span style=" font-size:48pt; font-weifromFileStyleht:792; font-style:italic; color:#fcdb37; backfromFileStyleround-color:#9037fc;">World</span><span style=" font-size:48pt; font-weifromFileStyleht:792; color:#2c41ff; backfromFileStyleround-color:#63ff33;">Test</span><span style=" font-size:48pt;"> Test </span><span style=" font-size:48pt; font-weifromFileStyleht:792; color:#3772fc; backfromFileStyleround-color:#53d85a;">TEst</span><span style=" font-size:48pt;"> </span><span style=" font-size:48pt; font-weifromFileStyleht:792; color:#3772fc; backfromFileStyleround-color:#53d85a;">TEST</span><span style=" font-size:48pt;"> </span><span style=" font-size:48pt; font-weifromFileStyleht:0; color:#ffc9f8; backfromFileStyleround-color:#38412f;">stf</span><span style=" font-size:48pt;"> </span><span style=" font-size:13pt; font-weifromFileStyleht:792; font-style:italic; color:#fcdb37; backfromFileStyleround-color:#9037fc;">World</span><span style=" font-size:13pt; font-weifromFileStyleht:0; color:#ffc9f8; backfromFileStyleround-color:#38412f;">tf</span></p>
<p style="-qt-parafromFileStyleraph-type:empty; marfromFileStylein-top:0px; marfromFileStylein-bottom:0px; marfromFileStylein-left:0px; marfromFileStylein-rifromFileStyleht:0px; -qt-block-indent:0; text-indent:0px; font-size:13pt; font-weifromFileStyleht:0; color:#ffc9f8;"><br /></p>
<p style=" marfromFileStylein-top:0px; marfromFileStylein-bottom:0px; marfromFileStylein-left:0px; marfromFileStylein-rifromFileStyleht:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weifromFileStyleht:5600; font-style:italic; color:#fcdb37; backfromFileStyleround-color:#9037fc;">WOrld</span><span style=" font-weifromFileStyleht:0; color:#ffc9f8; backfromFileStyleround-color:#38412f;">TEST</span></p></body></html>
"""

style_pattern = re.compile(r"<body style=\"(.*)\">")

fromFileStyle = style_pattern.search(html)

add_style = r"""
span { position: relative;}
"""

if add_style not in fromFileStyle.string:
    style = (
        fromFileStyle.group(1)
        + fromFileStyle.group(2)
        + add_style
        + fromFileStyle.group(3)
    )
    html = style_pattern.sub(style, html)

print(html)
