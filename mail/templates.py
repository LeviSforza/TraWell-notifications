CSS_STYLE = """

            .body {
                font-family: "Roboto";
                font-size: 16px;
                text-align: center;
                color: #06283D;
                background-color: rgb(254, 254, 254);
            }
            .header {
                width: 100%;
                height: 50px;
                background-color: white;
            }
            .logo {
                margin-top: 6px;
                float: right;
            }
            .blue-box {
                color: #F6F8FA;
                font-weight: 550;
                padding: 30px 10px 30px 30px;
                clear: right;
                margin-bottom: 20px;
            }
            .container {
                width: 100%;
                overflow: hidden;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .half-box {
                float: left;
            }
            .left {
                width: 60%;
                margin-top: 40px;
            }
            .right {
                width: 40%;
            }
            .picture {
                width: 250px;
                height: 250px;
                margin: 0 auto;
                display: inline-block;
            }
            .title {
                display: block;
                font-weight: 900;
                font-size: 22px;
                margin-bottom: 10px;
            }
            .contents {
                display: inline-block;
                margin-bottom: 20px;
            }
            .btn {
                display: block;
                width: fit-content;
                margin: 0 auto;
                border-radius: 10px;
                text-decoration: none;
            }
            .btn-inner {
                padding: 10px 14px 10px 14px;
                border-radius: 10px;
                background-color: #06283D;
                color: #F6F8FA;
                border: 1px solid #06283D;
                font-size: 14px;
                font-weight: 800;
                text-decoration: none;
            }
            .msg {
                clear: left;
                margin-left: 10px;
                margin-right: 10px;
                margin-bottom: 20px;
            }
            .msg_title {
                display: block;
                margin-bottom: 10px;
                text-align: left;
            }
            .msg_body {
                display: block;
                margin-bottom: 10px;
                text-align: justify;
            }
            .msg_signature {
                display: block;
                margin-bottom: 4px;
                text-align: right;
            }
            .line {
                border-top: 1px solid #06283D;
                width: 98%;
                margin: auto;
                padding-bottom: 20px;
            }
            .wrapper {
                margin-bottom: 20px;
            }
            .form-label {
                text-align: left;
                padding-left: 20px;
                padding-top: 6px;
                font-style: italic;
                font-weight: 700;
            }
            .form-input {
                text-align: left;
                padding-right: 20px;
                padding-left: 10px;
            }
            .table {
                margin: auto;
            }
            .star {
                font-size:150%;
                color: #FCA311;
            }
            .mailbox {
                font-size: 14px;
                font-style: italic;
            }
            .footer {
                background-color: #06283D;
                color: #F6F8FA;
                font-size: 12px;
                padding: 10px;
                margin: auto;
            }
            @media only screen and (max-width: 655px), only screen and (max-device-width: 655px) {
                #logo {
                    height: 36px;
                    width: 106px;
                }
                .blue-box {
                    padding: 10px 20px 10px 20px;
                }
                .title {
                    font-size: 20px;
                }
                .half-box {
                    float: unset;
                }
                .left {
                    width: 100%;
                }
                .right {
                    width: 100%;
                }
                .picture {
                    margin: 0 auto;
                    display: inline-block;
                }
                .btn {
                    margin: 0 auto 20px auto;
                }
            }
"""

HTML_BODY_USER = """
<!DOCTYPE html>
<html>
    <head>
        <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet" />
        <title>Request to join a ride</title>
        <style type="text/css">
            {{ css }}
        </style>
    </head>
    
    <body class="body">
        <div class="header">
            <div class="logo">
                <img height="40" width="118" id="logo" src={{ logo.src }}>
            </div>
        </div>

        <div class="blue-box" style="background-color: {{ box_color }};">
            <div class="container">
                <div class="half-box left">
                    <span class="title">{{ title }}</span>
                    <span class="contents">{{ content }}</span>
                    <div class="btn">
                        <a class="btn-inner" href="http://localhost:5173/" target="_blank" style="text-decoration:none !important; text-decoration:none; color:white">
                            SEE DETAILS
                        </a>
                    </div>
                </div>
                <div class="half-box right">
                    <div class="picture">
                        <img width="250" height="250" src={{ picture.src }}>
                    </div>
                </div>
            </div>
        </div>

        <div class="msg">
            <span class="msg_title">Hi!</span>
            <span class="msg_body">{{ message }}</span>
            <span class="msg_signature">Kind regards,</span>
            <span class="msg_signature">TraWell Team</span>
        </div>

        <div class="line"></div>

        <div class="wrapper">
            <span class="title">Basic passenger information:</span>
            <table class="table">
                <tr>
                    <td class="form-label">Name:</td>
                    <td class="form-input">{{ name }}</td>
                    <td class="form-label">Age:</td>
                    <td class="form-input">{{ age }}</td>
                  </tr>
                  <tr>
                    <td class="form-label">Rating:</td>
                    <td class="form-input">{{ avg_rate }}
                        <span class="star"> &#x2605; </span>
                    </td>
                    <td class="form-label">No. of seats:</td>
                    <td class="form-input">{{ seats }}</td>
                  </tr>
            </table>
        </div>

        <div class="line"></div>

        <div class="wrapper mailbox">
            <span class="contents">This message comes from an unmonitored mailbox.
                Please do not reply, and use the contact details put on our website.
            </span>
        </div>

        <div class="footer">
            <span class="copyright">Copyright 2022. Made with love by
                Klaudia, Julia, Monika, Justyna</span>
        </div>

    </body>
</html>
"""

HTML_BODY_RIDE = """
<!DOCTYPE html>
<html>
    <head>
        <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet" />
        <title>Request to join a ride</title>
        <style type="text/css">
            {{ css }}
        </style>
    </head>
    
    <body class="body">
        <div class="header">
            <div class="logo">
                <img height="40" width="118" id="logo" src="{{ logo.src }}">
            </div>
        </div>

        <div class="blue-box" style="background-color: {{ box_color }};">
            <div class="container">
                <div class="half-box left">
                    <span class="title">{{ title }}</span>
                    <span class="contents">{{ content }}</span>
                    <div class="btn">
                        <a class="btn-inner" href="http://localhost:5173/" target="_blank" style="text-decoration:none !important; text-decoration:none; color:white">
                            SEE DETAILS
                        </a>
                    </div>
                </div>
                <div class="half-box right">
                    <div class="picture">
                        <img width="250" height="250" src="{{ picture.src }}">
                    </div>
                </div>
            </div>
        </div>

        <div class="msg">
            <span class="msg_title">Hi!</span>
            <span class="msg_body">{{ message }}</span>
            <span class="msg_signature">Kind regards,</span>
            <span class="msg_signature">TraWell Team</span>
        </div>

        <div class="line"></div>

        <div class="wrapper">
            <span class="title">Basic ride information:</span>
            <table class="table">
                <tr>
                    <td class="form-label">From:</td>
                    <td class="form-input">{{ city_from }}</td>
                    <td class="form-label">To:</td>
                    <td class="form-input">{{ city_to }}</td>
                  </tr>
                  <tr>
                    <td class="form-label">Date:</td>
                    <td class="form-input">{{ ride_date }}</td>
                    <td class="form-label">Time:</td>
                    <td class="form-input">{{ ride_time }}</td>
                  </tr>
                  <tr>
                    <td class="form-label">Price:</td>
                    <td class="form-input">{{ price }} zł</td>
                    <td class="form-label">Driver:</td>
                    <td class="form-input">{{ driver }}</td>
                  </tr>
            </table>
        </div>

        <div class="line"></div>

        <div class="wrapper mailbox">
            <span class="contents">This message comes from an unmonitored mailbox.
                Please do not reply, and use the contact details put on our website.
            </span>
        </div>

        <div class="footer">
            <span class="copyright">Copyright 2022. Made with love by
                Klaudia, Julia, Monika, Justyna</span>
        </div>

    </body>
</html>
"""
