group = VGroup(
    MarkupText("<b>foo</b> <i>bar</i> <b><i>foobar</i></b>"),
    MarkupText("<s>foo</s> <u>bar</u>"
               "<big>big</big> <small>small</small>"),
    MarkupText('<gradient from="RED" to="YELLOW">colors</gradient>'),
).arrange(DOWN)
self.add(group)