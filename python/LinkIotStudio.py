from linkkit import linkkit

def on_connect(session_flag, rc, userdata):
    print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))
    pass


def on_disconnect(rc, userdata):
    print("on_disconnect:rc:%d,userdata:" % rc)

lk = linkkit.LinkKit(
    host_name="cn-shanghai",
    product_key="a1F83CGt9bR",
    device_name="RaPi",
    device_secret="324bfb97bf514e7ad2a1da23571f779e")

lk.on_connect = on_connect
lk.on_disconnect = on_disconnect
lk.connect_async()
