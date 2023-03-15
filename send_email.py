import smtplib
import ssl
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Class set up for the purpose of creating HTML email and sending to the support

class SendEmail:

    def set_up_connection(self, name, user_email, selected, additional_n):

        with open('store.txt') as f:
            take_encryption = f.readline()

        sender_email = "EV.lodz.dev@gmail.com"
        receiver_email_support = "EV.lodz.help@gmail.com"
        receiver_email_user = user_email
        password = base64.b64decode(take_encryption).decode("utf-8")

        message = MIMEMultipart("alternative")
        message["Subject"] = f"New Support Request - Category: {selected}"
        message["From"] = sender_email
        message["To"] = receiver_email_support

        # Create the plain-text and HTML version of your message
        text = f"""\
        Hi there {name},\n
        We have received your support email regarding the application.\n
        We understand that you requested support in area of {selected}\n
        Additional notes provided by you:\n
        {additional_n}
        We will try to respond to your email as soon as possible until then.\n
        Keep those batteries charged!
        """
        html = f"""\
<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Simple Transactional Email</title>
  </head>
  <body>
    <table style="margin-left: auto; margin-right: auto">
      <tr>
        <td>
          <div>

            <!-- START CENTERED WHITE CONTAINER -->
            <table role="presentation">

              <!-- START MAIN CONTENT AREA -->
              <tr>
                <td>
                  <table>
                    <tr>
                      <td>
                        <p style="font-family:georgia,garamond,serif;font-size:16px;font-style:italic;">
                        Hi there, {name}</p>
                        <p>We have received your support email regarding the application.
                           We understand that you requested support in area of {selected}
                        </p>
                        <p>Additional notes provided by you:
                        </p>
                        <table style="text-align: right">
                            <tr>
                              <td>
                                {additional_n}
                              </td>
                            </tr>
                        </table>
                        <p>We will try to respond to your email as soon as possible until then.</p>
                        <br>
                        <p style="font-family:georgia,garamond,serif;font-size:16px;font-style:italic;">
                          Keep those batteries charged!</p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

            <!-- END MAIN CONTENT AREA -->
            </table>
            <!-- END CENTERED WHITE CONTAINER -->

            <!-- START FOOTER -->
            <div style="background-color: #51FF80">
              <table style="margin-left: auto; margin-right: auto">
                <tr>
                  <td style="text-align: center;font-family: 'Arial'; font-size:12px;font-style: oblique">
                    EV LODZ Charging Stations for a whole city.
                    <br>You can always contact us under ev.lodz.help@gmail.com.
                  </td>
                </tr>
                <tr>
                  <td style="text-align: center;font-family: Nonchalance; font-size:30px;">
                    EV LODZ
                  </td>
                </tr>
              </table>
            </div>
            <!-- END FOOTER -->
            <p style="text-align: center;font-size:10px">Message generated automatically, please do not reply to it.</p>
          </div>
        </td>
      </tr>
    </table>
  </body>
</html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create a secure SSL context
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                # TODO: Send email here
                server.sendmail(
                    sender_email, receiver_email_support, message.as_string()
                )
                server.sendmail(
                    sender_email, receiver_email_user, message.as_string()
                )
                server.close()
            print('Email sent!')
        except Exception as exception:
            print("Error: %s!\n\n" % exception)
