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


# global function to instantiate a kamailio class object
# -- executed when kamailio app_python module is initialized
def mod_init():
    KSR.info("===== from Python mod init\n")
    # dumpObj(KSR)
    return kamailio()

class kamailio:

    def ksr_startup(self):
        KSR.log("INFO", "Python KEMI startup completed.\n")
        return 0

    def random_branch(self):
        return "z9hG4bK" + "".join(random.choices("abcdef0123456789", k=8))

    def random_user_agent(self):
        agents = [
            "Huawei-P40-Pro",
            "MI 10/Android",
            "Samsung-S20/OneUI",
            "iPhone12/14.4",
            "OPPO-FindX3"
        ]
        return random.choice(agents)

    def ksr_request_route(self, msg):
        method = KSR.pv.get("$rm")

        if method == "INVITE":
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
            return KSR.sl.send_reply(200, "OK")

        return KSR.tm.t_relay()
