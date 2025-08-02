import sys
import KSR as KSR
import random

# global variables corresponding to defined values (e.g., flags) in kamailio.cfg
FLT_ACC=1
FLT_ACCMISSED=2
FLT_ACCFAILED=3
FLT_NATS=5

FLB_NATB=6
FLB_NATSIPPING=7

def mod_init():
    KSR.info("===== from Python mod init\n")
    # dumpObj(KSR)
    return kamailio()

class kamailio:

    def __init__(self):
        KSR.info('===== kamailio.__init__\n')


    # executed when kamailio child processes are initialized
    def child_init(self, rank):
        KSR.info('===== kamailio.child_init(%d)\n' % rank)
        return 0

    def random_branch(self):
        return "z9hG4bK" + "".join(random.choices("abcdef0123456789", k=8))

    def random_user_agent(self):
        agents = [
            "Huawei-P40-Pro",
            "MI 10/Android",
            "Samsung-S20/OneUI",
        ]
        return random.choice(agents)

    def ksr_request_route(self, msg):
        method = KSR.pv.get("$rm")

        if method == "INVITE":
            auth_username = KSR.pv.get("$au")  # Auth username
            if auth_username is None:
                KSR.sl.send_reply(403, "No auth username")
                return -1

            ACCOUNT_TO_TRUNK = {
                "1001": "gw_trunk1",
                "1016": "gw_trunk2",
            }

            trunk = ACCOUNT_TO_TRUNK.get(auth_username)
            if not trunk:
                KSR.sl.send_reply(403, "Unknown account")
                return -1

            KSR.pv.setw("$ru", f"sip:{trunk}@192.168.139.212:5060")

            KSR.textopsx.remove_hf("Via")
            KSR.textopsx.append_hf(f"Via: SIP/2.0/UDP 58.60.1.1:5060;rport;branch={self.random_branch()}\r\n")

            KSR.textopsx.remove_hf("Contact")
            KSR.textopsx.append_hf("Contact: <sip:13888888888@10.19.32.7:5060>\r\n")

            KSR.textopsx.remove_hf("User-Agent")
            KSR.textopsx.append_hf(f"User-Agent: {self.random_user_agent()}\r\n")

            if KSR.rtpengine.rtpengine_offer() < 0:
                KSR.sl.send_reply(500, "RTPENGINE ERROR")
                return -1

            return KSR.tm.t_relay()

        elif method == "REGISTER":
            if not KSR.is_REGISTER():
                return 1
            if KSR.registrar.save("location", 0) < 0:
                KSR.sl.sl_reply_error()
            return -255

        return 1  # 所有未處理的方法預設 return

