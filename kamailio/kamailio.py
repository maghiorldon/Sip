import KSR
import random

def ksr_startup():
    KSR.log("INFO", "Python KEMI startup completed.\n")
    return 0

def random_branch():
    return "z9hG4bK" + "".join(random.choices("abcdef0123456789", k=8))

def random_user_agent():
    agents = [
        "Huawei-P40-Pro",
        "MI 10/Android",
        "Samsung-S20/OneUI",
        "iPhone12/14.4",
        "OPPO-FindX3"
    ]
    return random.choice(agents)

def ksr_request_route(msg):
    method = KSR.pv.get("$rm")

    if method == "INVITE":
        # 偽裝 Via
        KSR.textopsx.remove_hf("Via")
        branch_value = random_branch()
        KSR.textopsx.append_hf(f"Via: SIP/2.0/UDP 58.60.1.1:5060;rport;branch={branch_value}\r\n")

        # 偽裝 Contact
        KSR.textopsx.remove_hf("Contact")
        KSR.textopsx.append_hf("Contact: <sip:13888888888@10.19.32.7:5060>\r\n")

        # 偽裝 User-Agent
        KSR.textopsx.remove_hf("User-Agent")
        ua_value = random_user_agent()
        KSR.textopsx.append_hf(f"User-Agent: {ua_value}\r\n")

        # RTP 中繼
        if KSR.rtpengine.rtpengine_offer() < 0:
            KSR.sl.send_reply(500, "RTPENGINE ERROR")
            return -1

        return KSR.tm.t_relay()

    elif method == "REGISTER":
        return KSR.sl.send_reply(200, "OK")

    return KSR.tm.t_relay()
