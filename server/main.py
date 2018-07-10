from flask import Flask, render_template, request

HOST = '0.0.0.0'
PORT = '3000'
class QrFileClassifierApi(Flask):
    def __init__(self, name, *args, **kwargs):
        self.name = 'QrFileClassifier'
        Flask.__init__(self, name)
        self.configure_routes()
    
    def configure_routes(self):
        @self.route('/')
        def home(user=None):
            return user
        
        @self.route('/login')
        def login():
            return

        @self.errorhandler(404)
        def page_not_found(error):
            return render_template('not_found.html')

if __name__ == '__main__':
    server = QrFileClassifierApi(__name__)
    server.run(host=HOST, port=PORT)
