import time

from cls.post_mail import PostSend
# from cls.furnace_data import FurnaceData
from cls.furnace_io import FurnaceIO


def main():
    furnace_ip = input('\nInput the furnace IP:\t')
    furnace_port = input('Furnace PORT:\t')
    customer_email = input('Please input your e-mail:\t')
    print()

    # availability of furnace to read data
    furnace_on_line = False
    count_lost = 0

    furnace = FurnaceIO(ip=furnace_ip,
                        port=furnace_port)

    post_mail = PostSend(send_to=customer_email)

    print(post_mail.mail_send(subj='Furnace. Work comp.',
                              message='Start of the program.'))
    last_message = "Start"

    temperature_arrived = False
    last_sp = 0

    while True:
        if furnace.check_ping():
            count_lost = 0
            funace_data = furnace.get_current_data()
            print(funace_data)

            if (funace_data.temperature == funace_data.working_set_point):
                if not temperature_arrived:
                    print(
                        post_mail.mail_send(
                            subj='Furnace. Work comp.',
                            message=f"Temperature of Furnace {furnace_ip} "
                                    f"achived {funace_data.temperature}."
                                    f"\n Current conditions: {funace_data}"))
                    temperature_arrived = True

            if (funace_data.working_set_point != last_sp):
                print(
                    post_mail.mail_send(
                        subj='Furnace. Work comp.',
                        message=f"Temperature of Furnace {furnace_ip} "
                                f"started to change."
                                f"\n Current conditions: {funace_data}"))
                temperature_arrived = False

            last_sp = funace_data.working_set_point
            last_message = funace_data

        else:
            print("lost connection")
            count_lost += 1

            if furnace_on_line and count_lost == 3:
                furnace_on_line = False
                print(post_mail.mail_send(
                    subj='Furnace. Work comp.',
                    message=f"Furnace {furnace_ip} lost connection.\n"
                            f"The last data is: {last_message}."))

        time.sleep(10)


if __name__ == '__main__':
    main()
