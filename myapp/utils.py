from jnius import autoclass, java_method, PythonJavaClass

def get_token():
    FirebaseMessaging = autoclass('com.google.firebase.messaging.FirebaseMessaging')
    FirebaseMessaging.getInstance().getToken().addOnSuccessListener(MyTokenListener())

class MyTokenListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/tasks/OnSuccessListener']
    __javacontext__ = "app"

    @java_method("(Ljava/lang/Object;)V")
    def onSuccess(self, s):
        print(s)
