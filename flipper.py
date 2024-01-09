# import used modules
import odroid_wiringpi as wpi
import time
import webbrowser
from datetime import datetime
from random import randint
import mysql.connector
import sys

# Connecting to my personal database.
database = mysql.connector.connect(
         host="oege.ie.hva.nl",
         user="zwuupcm",
         password="mDxlEo6IcbwOtI",
         database="zzwuupcm",
)

# Import Flask module to run html on python.
from flask import Flask, render_template
from sensors.DHT11 import DHT11

# Making flask app.
app = Flask(__name__, static_url_path='', template_folder='.')

# Put the motors on the fartest flipStance.
def flipStance():

     servoSpin = 250
     wpi.pwmWrite(SERVO_PINL, servoSpin)
     wpi.pwmWrite(SERVO_PINR, servoSpin)
     print(servoSpin)
     return 'flip state'

# Put the motors on the fartest flipStance.
def neutralStance():

     servoSpinL = 400
     servoSpinR = 100
     wpi.pwmWrite(SERVO_PINL, servoSpinL)
     wpi.pwmWrite(SERVO_PINR, servoSpinR)
     print(servoSpinL)
     print(servoSpinR)
     return 'neutral state'

# Route to the home page
@app.route('/')
def home():
     # Database query for highscores.
     cursor = database.cursor()
     cursor.execute("SELECT timestamps, name, totalscore FROM score;")
     results = cursor.fetchall()
     cursor.close()

     p = []

     tbl =  "<th>timestamps</th><th>name</th><th>totalscore</th>"
     p.append(tbl)

     # this puts the information in the table.
     for row in results:
         p.append("  <tr>")
         p.append("    <td>%s</td>" % row[0])
         p.append("    <td>%s</td>" % row[1])
         p.append("    <td>%d PT</td>" % row[2])
         p.append("  </tr>")

     # My beautiful website.
     contents = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
  <style> 
    *::before,
    *::after,
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      scroll-behavior: smooth;
    }

    body {
      font-family: "Uni Sans W01 Regular";
      font-size: 1rem;
    }

    h1 {
      font-family: "Uni Sans Heavy Regular";
      color: #D81E05;
      font-size: 3.75rem;
    }

    h2 {
      font-family: "Uni Sans Heavy Regular";
      color: #666;
      font-size: 3rem;
    }

    table {
      background-color: #F5F5F5;
    }

    td {
      padding: 1rem;
      white-space: nowrap;
    }

    span {
      margin-right: .5rem;
      font-weight: bold;
    }

    header {
      padding-top: 1rem;
      padding-bottom: 1rem;
      padding-left: 2rem;
    }

    #hero {
      padding: 2rem;
      display: flex;
      flex-wrap: wrap;
      background-color: #F5F5F5;
      gap: 1.5rem;
    }

    .intro {
      width: 900px;
    }

    .intro p {
      font-size: 2rem;
    }

    .top-three {
      background-color: #fff;
    }

    .top-three h2 {
      margin-top: 1.5rem;
      margin-left: 1rem;
      color: #D81E05;
    }

    .top-three-table {
      margin-top: 1rem;
      background-color: #fff;
      border-top: 2px solid #D81E05;
    }

    .top-three-table td:first-child {
      min-width: 315px;
    }

    .top-three-table td,
    .top-three-table td:first-child {
      background-color: #fff;
    }

    #all-highscores {
      padding: 2rem;
    }

     .highscores {
      padding-top: 1rem;
      color: #fff;
      display: flex;
      overflow-x: auto;
      gap: 35px;
      flex-direction: row-reverse;
    }

    .highscores table {
      color: #000;
    }

    .highscores th {
      padding: 1rem;
      text-align: left;
    }
    
    .highscores td:first-child {
      background-color: #F5F5F5;
      min-width: 398px;
    }
  </style>
  <link href="https://db.onlinewebfonts.com/c/4f6fb2fa3c231278167b36e966718cbb?family=Uni+Sans+Heavy+Regular" rel="stylesheet">
  <link href="https://db.onlinewebfonts.com/c/ab804af7699fabaf769911c77bb4d115?family=Uni+Sans+W01+Regular" rel="stylesheet">
</head>
<header>
  <svg width="302.139008" height="32.146759" viewBox="0 0 302.139 32.1468" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <defs/>
    <path id="corendon flipperkast." d="M14.3983 20.6624C13.9312 21.6935 13.3757 22.548 12.7321 23.2259C12.094 23.8981 11.4247 24.4392 10.724 24.8494C10.0233 25.2596 9.31122 25.5501 8.58777 25.721C7.86426 25.8976 7.19775 25.9859 6.58826 25.9859C5.6825 25.9859 4.80237 25.8463 3.94788 25.5672C3.09906 25.288 2.35852 24.875 1.7262 24.3282C1.09955 23.7756 0.626709 23.0863 0.307739 22.2603C-0.00561523 21.4286 -0.0796509 20.4659 0.0855713 19.3721L0.922974 13.459C1.08813 12.3368 1.43848 11.3798 1.974 10.5879C2.50946 9.79041 3.16174 9.14099 3.93079 8.63968C4.69983 8.13837 5.55145 7.76526 6.48572 7.52029C7.41992 7.27533 8.34277 7.15286 9.25427 7.15286C9.85809 7.15286 10.4875 7.22977 11.1427 7.38358C11.7978 7.53738 12.4102 7.80798 12.9799 8.19534C13.5495 8.57703 14.0394 9.08401 14.4496 9.71634C14.8597 10.343 15.1332 11.1462 15.2699 12.126L10.0917 13.6641C10.0461 13.1286 9.86951 12.7384 9.56189 12.4934C9.25995 12.2485 8.92383 12.126 8.55359 12.126C8.13202 12.126 7.73328 12.2542 7.3573 12.5105C6.987 12.7669 6.7677 13.1514 6.69934 13.6641L5.85339 19.4746C5.78503 19.9645 5.90179 20.3434 6.20374 20.6111C6.51135 20.8788 6.86169 21.0127 7.25476 21.0127C7.6535 21.0127 8.05511 20.8959 8.45959 20.6624C8.86975 20.4288 9.203 20.0443 9.45935 19.5088L14.3983 20.6624Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M17.0246 13.8435C17.1841 12.7213 17.5316 11.7472 18.0671 10.9212C18.6083 10.0895 19.269 9.39447 20.0495 8.83621C20.83 8.27795 21.6816 7.85925 22.6044 7.58011C23.5273 7.29529 24.4558 7.15286 25.3901 7.15286C26.2958 7.15286 27.1731 7.29529 28.0219 7.58011C28.8764 7.85925 29.6056 8.27795 30.2094 8.83621C30.819 9.39447 31.2804 10.0895 31.5937 10.9212C31.9127 11.7472 31.9896 12.7213 31.8244 13.8435L31.0212 19.5772C30.8845 20.6538 30.5398 21.5881 29.9872 22.3799C29.4404 23.1718 28.7824 23.8383 28.0134 24.3794C27.2443 24.9149 26.3984 25.3165 25.4755 25.5843C24.5527 25.852 23.6241 25.9859 22.6899 25.9859C21.7841 25.9859 20.904 25.852 20.0495 25.5843C19.2007 25.3165 18.4658 24.9149 17.8449 24.3794C17.224 23.8383 16.7626 23.166 16.4606 22.3628C16.1587 21.5596 16.079 20.631 16.2214 19.5772L17.0246 13.8435ZM24.5783 12.408C24.2308 12.408 23.8634 12.5248 23.476 12.7583C23.0944 12.9919 22.8807 13.3166 22.8351 13.7325L22.0234 19.6541C21.9778 20.0699 22.0946 20.4003 22.3737 20.6453C22.6586 20.8903 22.9975 21.0127 23.3906 21.0127C23.7893 21.0127 24.1682 20.9102 24.527 20.7051C24.8916 20.4943 25.1081 20.144 25.1765 19.6541L25.9797 13.7325C26.0309 13.3166 25.8971 12.9919 25.5781 12.7583C25.2648 12.5248 24.9315 12.408 24.5783 12.408Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M42.816 7.15286C43.1464 7.15286 43.5366 7.1842 43.9866 7.24686C44.4424 7.30383 45.0433 7.4263 45.7896 7.61429L45.0889 12.5447C44.6959 12.408 44.2487 12.3282 43.7474 12.3055C43.2461 12.277 42.7618 12.3282 42.2947 12.4593C41.8276 12.5846 41.4175 12.8011 41.0643 13.1087C40.7168 13.4106 40.5089 13.8065 40.4405 14.2964L38.8597 25.6355L32.9466 25.6355L34.5189 14.2281C34.6841 12.9919 35.0059 11.9295 35.4844 11.0408C35.963 10.1521 36.564 9.41727 37.2874 8.83621C38.0109 8.25516 38.8397 7.83075 39.774 7.56302C40.7083 7.28958 41.7222 7.15286 42.816 7.15286Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M51.5308 18.8423C51.4397 19.5202 51.5679 20.0471 51.9153 20.4231C52.2686 20.7934 52.7186 21.027 53.2654 21.1238C53.8123 21.215 54.3934 21.1808 55.0086 21.0213C55.6295 20.8561 56.1508 20.5741 56.5723 20.1753L59.4092 23.0464C58.7769 23.673 58.1503 24.1801 57.5294 24.5674C56.9141 24.9548 56.3018 25.2538 55.6922 25.4646C55.0884 25.6697 54.4988 25.8064 53.9234 25.8748C53.3538 25.9489 52.8126 25.9859 52.2999 25.9859C51.3941 25.9859 50.5197 25.8406 49.6766 25.5501C48.8392 25.2596 48.11 24.8351 47.4891 24.2769C46.8738 23.7129 46.4067 23.0122 46.0877 22.1748C45.7744 21.3317 45.7003 20.3633 45.8655 19.2696L46.6004 14.0828C46.7599 12.9435 47.1074 11.9437 47.6429 11.0835C48.1841 10.2177 48.8448 9.49417 49.6253 8.91312C50.4058 8.32635 51.2631 7.88773 52.1973 7.5972C53.1316 7.30096 54.0658 7.15286 55.0001 7.15286C55.9343 7.15286 56.803 7.29529 57.6063 7.58011C58.4095 7.85925 59.0902 8.27225 59.6485 8.81912C60.2125 9.366 60.6226 10.0553 60.879 10.887C61.1353 11.713 61.1809 12.6871 61.0157 13.8094C60.8562 14.8803 60.4717 15.7889 59.8621 16.5352C59.2583 17.2814 58.512 17.8654 57.6234 18.2869C56.7347 18.7084 55.7606 18.9648 54.701 19.0559C53.6414 19.1471 52.5847 19.0759 51.5308 18.8423ZM52.0948 15.3474C52.4423 15.507 52.8211 15.5952 53.2313 15.6123C53.6414 15.6237 54.0203 15.5639 54.3677 15.4329C54.7152 15.3019 55.0115 15.0968 55.2564 14.8177C55.5013 14.5385 55.6495 14.1654 55.7007 13.6983C55.7691 13.2824 55.6922 12.9008 55.47 12.5533C55.2479 12.2001 54.8577 12.0235 54.2994 12.0235C53.8778 12.0235 53.462 12.163 53.0518 12.4422C52.6473 12.7213 52.4081 13.1172 52.334 13.6299L52.0948 15.3474Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M64.2382 8.62259C65.2635 8.15546 66.3658 7.79373 67.545 7.53738C68.7242 7.28104 69.9091 7.15286 71.0997 7.15286C72.1935 7.15286 73.2131 7.27533 74.1588 7.52029C75.1044 7.76526 75.9077 8.15833 76.5685 8.69949C77.235 9.23499 77.7192 9.93567 78.0211 10.8015C78.3287 11.6617 78.3999 12.7213 78.2347 13.9803L76.5941 25.6355L70.7152 25.6355L72.3558 14.0144C72.4526 13.3593 72.3359 12.9178 72.0055 12.69C71.6808 12.4564 71.2849 12.3396 70.8177 12.3396C70.3506 12.3396 69.9433 12.408 69.5958 12.5447L67.7416 25.6355L61.8199 25.6355L64.2382 8.62259Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M94.4457 24.4478C93.3007 24.8636 92.0617 25.2254 90.7287 25.533C89.4014 25.8349 88.0712 25.9859 86.7382 25.9859C85.7869 25.9859 84.8783 25.8748 84.0124 25.6526C83.1465 25.4305 82.4088 25.0687 81.7993 24.5674C81.1954 24.0661 80.7426 23.3968 80.4406 22.5594C80.1387 21.7162 80.0817 20.6766 80.2697 19.4405L81.1413 13.2454C81.2838 12.2428 81.5885 11.357 82.0556 10.5879C82.5228 9.81888 83.0924 9.18372 83.7646 8.6824C84.4425 8.17542 85.1945 7.79373 86.0204 7.53738C86.8522 7.28104 87.7123 7.15286 88.601 7.15286C88.9941 7.15286 89.3815 7.1842 89.7631 7.24686C90.1505 7.30383 90.5322 7.38928 90.9081 7.5032L91.8139 0.855255L97.7697 0.855255L94.4457 24.4478ZM90.2075 12.2627C89.9283 12.126 89.5552 12.0576 89.0881 12.0576C88.621 12.0576 88.171 12.1801 87.738 12.4251C87.3051 12.67 87.043 13.0717 86.9518 13.6299L86.0461 19.9275C85.972 20.4687 86.1259 20.8504 86.5075 21.0725C86.8949 21.289 87.3336 21.3972 87.8234 21.3972C88.1766 21.3972 88.5526 21.3403 88.9514 21.2263L90.2075 12.2627Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M98.7846 13.8435C98.9441 12.7213 99.2916 11.7472 99.8271 10.9212C100.368 10.0895 101.029 9.39447 101.81 8.83621C102.59 8.27795 103.442 7.85925 104.364 7.58011C105.287 7.29529 106.216 7.15286 107.15 7.15286C108.056 7.15286 108.933 7.29529 109.782 7.58011C110.636 7.85925 111.366 8.27795 111.969 8.83621C112.579 9.39447 113.04 10.0895 113.354 10.9212C113.673 11.7472 113.75 12.7213 113.584 13.8435L112.781 19.5772C112.644 20.6538 112.3 21.5881 111.747 22.3799C111.2 23.1718 110.542 23.8383 109.773 24.3794C109.004 24.9149 108.158 25.3165 107.236 25.5843C106.313 25.852 105.384 25.9859 104.45 25.9859C103.544 25.9859 102.664 25.852 101.81 25.5843C100.961 25.3165 100.226 24.9149 99.6049 24.3794C98.9839 23.8383 98.5225 23.166 98.2206 22.3628C97.9187 21.5596 97.8389 20.631 97.9814 19.5772L98.7846 13.8435ZM106.338 12.408C105.991 12.408 105.623 12.5248 105.236 12.7583C104.854 12.9919 104.641 13.3166 104.595 13.7325L103.783 19.6541C103.738 20.0699 103.855 20.4003 104.134 20.6453C104.419 20.8903 104.758 21.0127 105.151 21.0127C105.549 21.0127 105.928 20.9102 106.287 20.7051C106.652 20.4943 106.868 20.144 106.936 19.6541L107.74 13.7325C107.791 13.3166 107.657 12.9919 107.338 12.7583C107.025 12.5248 106.691 12.408 106.338 12.408Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M117.193 8.62259C118.219 8.15546 119.321 7.79373 120.5 7.53738C121.679 7.28104 122.864 7.15286 124.055 7.15286C125.148 7.15286 126.168 7.27533 127.114 7.52029C128.059 7.76526 128.863 8.15833 129.523 8.69949C130.19 9.23499 130.674 9.93567 130.976 10.8015C131.284 11.6617 131.355 12.7213 131.19 13.9803L129.549 25.6355L123.67 25.6355L125.311 14.0144C125.408 13.3593 125.291 12.9178 124.961 12.69C124.636 12.4564 124.24 12.3396 123.773 12.3396C123.306 12.3396 122.898 12.408 122.551 12.5447L120.697 25.6355L114.775 25.6355L117.193 8.62259Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M158.874 25.4646C157.615 25.7893 156.478 25.8406 155.464 25.6184C154.45 25.3963 153.604 24.9776 152.926 24.3623C152.249 23.7414 151.759 22.9581 151.457 22.0125C151.155 21.0668 151.086 20.0101 151.252 18.8423L153.764 0.855255L159.685 0.855255L157.165 18.774C157.091 19.3094 157.253 19.7538 157.652 20.107C158.051 20.4545 158.703 20.5228 159.609 20.312L158.874 25.4646ZM137.597 27.524C137.996 27.2448 138.306 26.9828 138.528 26.7378C138.75 26.4929 138.913 26.2593 139.015 26.0371C139.118 25.815 139.181 25.6184 139.203 25.4475C139.232 25.2709 139.257 25.1115 139.28 24.969L141.69 7.81937C141.878 6.4408 142.274 5.27014 142.878 4.3074C143.487 3.33899 144.239 2.56424 145.133 1.98318C146.034 1.39642 147.039 1.00336 148.15 0.803986C149.261 0.604614 150.423 0.587524 151.636 0.752716L150.901 6.10184C150.434 5.98792 150.001 5.95941 149.602 6.01639C149.204 6.07336 148.853 6.19012 148.551 6.36673C148.25 6.54333 148.005 6.7598 147.817 7.01614C147.629 7.27249 147.512 7.54022 147.466 7.81937L147.364 8.41751L150.406 8.41751L149.671 13.6299L146.629 13.6299L145.057 24.969C144.891 26.1596 144.393 27.2847 143.561 28.3443C142.735 29.4095 141.516 30.3979 139.904 31.3094L137.597 27.524Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M163.429 3.27347C163.52 2.52722 163.771 1.91483 164.181 1.43631C164.591 0.957794 165.064 0.596069 165.6 0.351105C166.135 0.10614 166.699 -0.0106201 167.292 0.000762939C167.89 0.012146 168.422 0.14032 168.89 0.385284C169.357 0.630249 169.718 0.991974 169.975 1.47049C170.231 1.94901 170.311 2.54999 170.214 3.27347C170.123 3.94568 169.878 4.50964 169.479 4.96536C169.086 5.42108 168.619 5.76004 168.078 5.98221C167.542 6.20438 166.984 6.32117 166.403 6.33255C165.822 6.34393 165.292 6.23856 164.814 6.01639C164.335 5.79422 163.959 5.45813 163.686 5.00809C163.418 4.55237 163.332 3.97415 163.429 3.27347ZM169.24 7.5032L166.685 25.6355L160.763 25.6355L163.318 7.5032L169.24 7.5032Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M172.354 8.69949C173.522 8.27795 174.781 7.9162 176.131 7.61429C177.487 7.30667 178.817 7.15286 180.121 7.15286C181.101 7.15286 182.004 7.25256 182.83 7.45193C183.662 7.65131 184.368 7.99597 184.949 8.48587C185.536 8.97577 185.975 9.61951 186.265 10.417C186.556 11.2089 186.655 12.1972 186.564 13.3821L185.718 19.4405C185.582 20.5399 185.274 21.4912 184.795 22.2945C184.317 23.0977 183.744 23.7699 183.078 24.3111C182.417 24.8466 181.676 25.2425 180.856 25.4988C180.042 25.7552 179.224 25.8833 178.404 25.8833C177.988 25.8833 177.575 25.852 177.165 25.7893C176.755 25.7324 176.353 25.6469 175.96 25.533L175.011 32.1468L169.098 32.1468L172.354 8.69949ZM176.626 20.7735C176.997 20.9557 177.461 21.0469 178.019 21.0469C178.464 21.0469 178.859 20.933 179.207 20.7051C179.56 20.4716 179.782 20.0272 179.874 19.3721L180.754 13.2112C180.822 12.6985 180.685 12.3254 180.343 12.0918C180.007 11.8583 179.583 11.7415 179.07 11.7415C178.859 11.7415 178.649 11.7529 178.438 11.7757C178.233 11.7985 178.036 11.844 177.848 11.9124L176.626 20.7735Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M190.099 8.69949C191.267 8.27795 192.526 7.9162 193.876 7.61429C195.232 7.30667 196.562 7.15286 197.866 7.15286C198.846 7.15286 199.749 7.25256 200.575 7.45193C201.407 7.65131 202.113 7.99597 202.694 8.48587C203.281 8.97577 203.72 9.61951 204.01 10.417C204.301 11.2089 204.4 12.1972 204.309 13.3821L203.463 19.4405C203.327 20.5399 203.019 21.4912 202.54 22.2945C202.062 23.0977 201.489 23.7699 200.823 24.3111C200.162 24.8466 199.421 25.2425 198.601 25.4988C197.787 25.7552 196.969 25.8833 196.149 25.8833C195.733 25.8833 195.32 25.852 194.91 25.7893C194.5 25.7324 194.098 25.6469 193.705 25.533L192.756 32.1468L186.843 32.1468L190.099 8.69949ZM194.371 20.7735C194.742 20.9557 195.206 21.0469 195.764 21.0469C196.209 21.0469 196.604 20.933 196.952 20.7051C197.305 20.4716 197.527 20.0272 197.618 19.3721L198.499 13.2112C198.567 12.6985 198.43 12.3254 198.088 12.0918C197.752 11.8583 197.328 11.7415 196.815 11.7415C196.604 11.7415 196.394 11.7529 196.183 11.7757C195.978 11.7985 195.781 11.844 195.593 11.9124L194.371 20.7735Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M211.621 18.8423C211.53 19.5202 211.658 20.0471 212.005 20.4231C212.359 20.7934 212.809 21.027 213.355 21.1238C213.902 21.215 214.483 21.1808 215.099 21.0213C215.72 20.8561 216.241 20.5741 216.662 20.1753L219.499 23.0464C218.867 23.673 218.24 24.1801 217.619 24.5674C217.004 24.9548 216.392 25.2538 215.782 25.4646C215.178 25.6697 214.589 25.8064 214.013 25.8748C213.444 25.9489 212.903 25.9859 212.39 25.9859C211.484 25.9859 210.61 25.8406 209.767 25.5501C208.929 25.2596 208.2 24.8351 207.579 24.2769C206.964 23.7129 206.497 23.0122 206.178 22.1748C205.864 21.3317 205.79 20.3633 205.956 19.2696L206.69 14.0828C206.85 12.9435 207.197 11.9437 207.733 11.0835C208.274 10.2177 208.935 9.49417 209.715 8.91312C210.496 8.32635 211.353 7.88773 212.287 7.5972C213.222 7.30096 214.156 7.15286 215.09 7.15286C216.024 7.15286 216.893 7.29529 217.696 7.58011C218.499 7.85925 219.18 8.27225 219.738 8.81912C220.302 9.366 220.713 10.0553 220.969 10.887C221.225 11.713 221.271 12.6871 221.106 13.8094C220.946 14.8803 220.562 15.7889 219.952 16.5352C219.348 17.2814 218.602 17.8654 217.713 18.2869C216.825 18.7084 215.851 18.9648 214.791 19.0559C213.731 19.1471 212.675 19.0759 211.621 18.8423ZM212.185 15.3474C212.532 15.507 212.911 15.5952 213.321 15.6123C213.731 15.6237 214.11 15.5639 214.458 15.4329C214.805 15.3019 215.101 15.0968 215.346 14.8177C215.591 14.5385 215.739 14.1654 215.791 13.6983C215.859 13.2824 215.782 12.9008 215.56 12.5533C215.338 12.2001 214.948 12.0235 214.389 12.0235C213.968 12.0235 213.552 12.163 213.142 12.4422C212.737 12.7213 212.498 13.1172 212.424 13.6299L212.185 15.3474Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M231.711 7.15286C232.041 7.15286 232.432 7.1842 232.882 7.24686C233.337 7.30383 233.938 7.4263 234.685 7.61429L233.984 12.5447C233.591 12.408 233.144 12.3282 232.642 12.3055C232.141 12.277 231.657 12.3282 231.19 12.4593C230.723 12.5846 230.312 12.8011 229.959 13.1087C229.612 13.4106 229.404 13.8065 229.335 14.2964L227.755 25.6355L221.842 25.6355L223.414 14.2281C223.579 12.9919 223.901 11.9295 224.379 11.0408C224.858 10.1521 225.459 9.41727 226.182 8.83621C226.906 8.25516 227.735 7.83075 228.669 7.56302C229.603 7.28958 230.617 7.15286 231.711 7.15286Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M246.382 7.5032L253.03 7.5032L245.22 16.2874L250.475 25.6355L243.895 25.6355L240.776 19.825L239.973 25.6355L234.333 25.6355L237.803 0.855255L243.434 0.855255L241.725 13.1429L246.382 7.5032Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M260.688 24.3025C260.062 24.8437 259.381 25.2596 258.646 25.5501C257.911 25.8406 257.227 25.9859 256.595 25.9859C255.758 25.9859 255.006 25.8235 254.339 25.4988C253.673 25.1684 253.123 24.7184 252.69 24.1487C252.263 23.579 251.955 22.904 251.767 22.1236C251.579 21.3374 251.545 20.4772 251.665 19.543L252.434 13.9119C252.599 12.653 252.961 11.5934 253.519 10.7332C254.077 9.86731 254.758 9.1723 255.561 8.64822C256.37 8.11844 257.259 7.73676 258.227 7.5032C259.196 7.26965 260.181 7.15286 261.184 7.15286C262.329 7.15286 263.488 7.31805 264.662 7.64847C265.841 7.97318 266.943 8.43744 267.968 9.04129L265.695 25.6355L261.355 25.6355L260.688 24.3025ZM261.773 12.2627C261.426 12.1032 261.041 12.0235 260.62 12.0235C260.039 12.0235 259.52 12.1915 259.065 12.5276C258.609 12.8637 258.335 13.3138 258.244 13.8777L257.509 19.0901C257.464 19.4376 257.481 19.7367 257.561 19.9873C257.64 20.2323 257.754 20.426 257.902 20.5684C258.056 20.7051 258.244 20.8076 258.466 20.876C258.689 20.9444 258.917 20.9785 259.15 20.9785C259.714 20.9785 260.204 20.8732 260.62 20.6624L261.773 12.2627Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M271.545 19.543C272.103 20.0101 272.721 20.3605 273.399 20.594C274.077 20.8276 274.718 20.9216 275.322 20.876C275.624 20.8532 275.852 20.7535 276.006 20.5769C276.159 20.4003 276.228 20.2095 276.211 20.0044C276.199 19.7936 276.111 19.6057 275.946 19.4405C275.786 19.2753 275.544 19.1813 275.219 19.1585C274.194 18.9705 273.337 18.6629 272.647 18.2356C271.958 17.8027 271.408 17.2957 270.998 16.7146C270.594 16.1279 270.32 15.4984 270.178 14.8262C270.035 14.1483 270.013 13.4704 270.11 12.7925C270.201 12.0235 270.431 11.2943 270.802 10.605C271.178 9.91571 271.668 9.32043 272.271 8.81912C272.881 8.31781 273.604 7.9162 274.442 7.61429C275.285 7.30667 276.219 7.15286 277.245 7.15286C278.065 7.15286 278.993 7.30667 280.03 7.61429C281.067 7.9162 282.087 8.5343 283.089 9.46854L279.911 13.2112C278.879 12.6757 278.031 12.3909 277.364 12.3567C276.703 12.3168 276.29 12.4849 276.125 12.8609C276.034 13.0717 276.023 13.2539 276.091 13.4077C276.159 13.5558 276.27 13.6897 276.424 13.8094C276.578 13.9233 276.752 14.023 276.945 14.1084C277.145 14.1882 277.327 14.2394 277.492 14.2622C278.073 14.3762 278.66 14.5613 279.253 14.8177C279.851 15.074 280.383 15.4243 280.851 15.8687C281.318 16.313 281.674 16.8741 281.919 17.552C282.164 18.2299 282.218 19.0331 282.081 19.9617C281.939 20.9928 281.639 21.8871 281.184 22.6448C280.728 23.4025 280.167 24.0262 279.5 24.5161C278.84 25.006 278.093 25.3735 277.262 25.6184C276.436 25.8634 275.59 25.9859 274.724 25.9859C274.12 25.9859 273.536 25.9431 272.972 25.8577C272.414 25.778 271.867 25.6355 271.331 25.4305C270.796 25.2197 270.278 24.9348 269.776 24.576C269.275 24.2114 268.802 23.7357 268.358 23.149L271.545 19.543Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M293 25.3194C291.832 25.7637 290.675 25.9859 289.53 25.9859C288.693 25.9859 287.93 25.8463 287.24 25.5672C286.551 25.288 285.979 24.8693 285.523 24.3111C285.067 23.7471 284.745 23.035 284.557 22.1748C284.375 21.309 284.364 20.2921 284.523 19.1243L286.77 3.23929L292.333 3.23929L292.017 7.5032L294.991 7.5032L294.358 11.9124L291.385 11.9124L290.411 19.0901C290.291 19.8136 290.399 20.2978 290.735 20.5428C291.077 20.7877 291.504 20.9102 292.017 20.9102C292.484 20.9102 293.034 20.8162 293.666 20.6282L293 25.3194Z" fill-rule="nonzero" fill="#D81E05"/>
    <path id="corendon flipperkast." d="M295.133 22.3116C295.202 21.8217 295.358 21.3659 295.603 20.9444C295.848 20.5228 296.144 20.1554 296.492 19.8421C296.845 19.5287 297.244 19.2838 297.688 19.1072C298.132 18.9306 298.6 18.8423 299.089 18.8423C300.069 18.8423 300.85 19.1756 301.431 19.8421C302.018 20.5086 302.24 21.3317 302.097 22.3116C302.029 22.8015 301.872 23.2629 301.627 23.6958C301.382 24.1231 301.078 24.4962 300.713 24.8152C300.354 25.1285 299.953 25.3792 299.508 25.5672C299.064 25.7552 298.597 25.8492 298.107 25.8492C297.617 25.8492 297.173 25.7552 296.774 25.5672C296.381 25.3792 296.05 25.1285 295.783 24.8152C295.515 24.4962 295.321 24.1231 295.202 23.6958C295.088 23.2629 295.065 22.8015 295.133 22.3116Z" fill-rule="nonzero" fill="#FFC61E"/>
  </svg>  
</header>
<body>
  <section id="hero">
    <article class="intro">
      <h1>Speel het ultieme flipperkast spel tijdens het wachten!</h1>
      <p>Speel de flipperkast en word een flipperkastkampioen</p>
    </article>
    <article class="top-three">
      <h2>Top 3 Highscores</h2>
      <table class="top-three-table">
        <tr>
          <td><span>01</span> Jack Zwuup</td>
          <td>500 PT</td>
        </tr>
        <tr>
          <td><span>02</span> Daphne Zwuup</td>
          <td>482 PT</td>
        </tr>
        <tr>
          <td><span>03</span> Peter Zwuup</td>
          <td>458 PT</td>
        </tr>
      </table>
    </article>
  </section>

  <section id="all-highscores">
    <h2>Alle Highscores</h2>
      <div class="highscores">
        <table>
          %s
        </table>
      </div>
  </section>
</body>
</html>
     '''%(p)

     # Make uo a file name.
     filename = 'index.html'

    # Define the main function for writing the HTML content to a file
     def main(contents, filename):
       output = open(filename,"w")
       output.write(contents)
       output.close()

     # Call the main function to create the HTML file
     main(contents, filename)    

     # Open the HTML file in a web browser
     webbrowser.open(filename)
    
     # Return a rendered template (this is part of the Flask application)
     return render_template('index.html')

# Define a route for displaying temperature and humidity data.
@app.route('/temphumi')
def temphumi():
     cursor = database.cursor()
     cursor.execute("SELECT timestamps, temperatuur, vochtigheid FROM tempVocht;")

     results = cursor.fetchall()

     cursor.close()

     p = []
     
     # Create the table header.
     tbl =  "<th>timestamps</th><th>temperatuur</th><th>vochtigheid</th>"
     p.append(tbl)

     # Loop through the results and create table rows.
     for row in results:
         a = "<tr><td>%s</td>"%row[0]
         p.append(a)
         b = "<td>%s C</td>"%row[1]
         p.append(b)
         c = "<td>%s %%</td></tr>"%row[2]
         p.append(c)

     # Define the HTML content for displaying temperature and humidity data.
     contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
         <html>
         <head>
             <style>
                  body {
                    background-color: rgb(85, 105, 185);
                     }

                   th {
                   text-align: left;
                  }

                   th, td {
          padding: .5em
          }

          table, th, td {
            background-color: rgb(247, 199, 252);
            border-width: 5px;
            border: 3px solid #000;
               }     
             </style>         
         <meta content="text/html; charset=ISO-8859-1"
         http-equiv="content-type">
         <title>Python Webbrowser</title>
        </head>
        <body>
         <table>
         %s
         </table>
     </body>
     </html>

     '''%(p)

     filename = 'temphumi.html'

     def main(contents, filename):
       output = open(filename,"w")
       output.write(contents)
       output.close()

     main(contents, filename)    
     webbrowser.open(filename)
     return render_template('temphumi.html')

# Run the neutral stance function and make sure that the flipper is in the neutral stance.
@app.route('/ntrl')
def easy():
    return neutralStance()

# Run the flip stance function and make sure that the flipper is in the neutral stance.
@app.route('/flip')
def hard():
    return flipStance()



if __name__ == '__main__':

   BUTTON_PINL = 8  # Button pin for left button (Physical Pin 3)
   BUTTON_PINR = 9  # Button pin for right button (Physical Pin 5)
   BUTTON_PIN_ON = 30  # Button pin for turning on (Physical Pin 27)
   BUTTON_PIN_OFF = 31  # Button pin for turning off (Physical Pin 28)

   SERVO_PINL = 24  # Servo motor pin for left (Physical Pin 35, PWM)
   SERVO_PINR = 1   # Servo motor pin for right (Physical Pin 33, PWM)

   LASER_PIN1 = 0  # Laser pin 1 (Physical Pin 11)
   LASER_PIN2 = 2  # Laser pin 2 (Physical Pin 13)
   LASER_PIN3 = 3  # Laser pin 3 (Physical Pin 15)
   LASER_PIN4 = 4  # Laser pin 4 (Physical Pin 16)
   LASER_PIN5 = 5  # Laser pin 5 (Physical Pin 18)

   V1_PIN = 6  # Voltage pin 1 middle pin of ldr (Physical Pin 22)
   V2_PIN = 22  # Voltage pin 2 middle pin of ldr (Physical Pin 31)
   V3_PIN = 26  # Voltage pin 3 middle pin of ldr (Physical Pin 32)
   V4_PIN = 27  # Voltage pin 4 middle pin of ldr (Physical Pin 36)

   LDR_PIN1 = 10  # Light Dependent Resistor (LDR) pin 1 (GPIO Pin 10, connected to S = 24, M = 3.3V)
   LDR_PIN2 = 11  # LDR pin 2 (GPIO Pin 11, connected to S = 26)
   LDR_PIN3 = 12  # LDR pin 3 (GPIO Pin 12, connected to S = 19)
   LDR_PIN4 = 13  # LDR pin 4 (GPIO Pin 13, connected to S = 21)
   LDR_PIN5 = 14  # LDR pin 5 (GPIO Pin 14, connected to S = 23)

   LED_PIN = 15  # LED pin (Physical Pin 10)

   # Pin setup
   wpi.wiringPiSetup()
   wpi.pinMode(BUTTON_PINL, wpi.INPUT)  # Set left button pin to input
   wpi.pinMode(BUTTON_PINR, wpi.INPUT)  # Set right button pin to input
   wpi.pinMode(BUTTON_PIN_ON, wpi.INPUT)  # Set turn-on button pin to input
   wpi.pinMode(BUTTON_PIN_OFF, wpi.INPUT)  # Set turn-off button pin to input

   wpi.pinMode(SERVO_PINL, wpi.PWM_OUTPUT)  # Set left servo pin to output
   wpi.pinMode(SERVO_PINR, wpi.PWM_OUTPUT)  # Set right servo pin to output

   wpi.pinMode(LASER_PIN1, wpi.OUTPUT)  # Set laser pin 1 to output
   wpi.pinMode(LASER_PIN2, wpi.OUTPUT)  # Set laser pin 2 to output
   wpi.pinMode(LASER_PIN3, wpi.OUTPUT)  # Set laser pin 3 to output
   wpi.pinMode(LASER_PIN4, wpi.OUTPUT)  # Set laser pin 4 to output
   wpi.pinMode(LASER_PIN5, wpi.OUTPUT)  # Set laser pin 5 to output

   wpi.pinMode(V1_PIN, wpi.OUTPUT)  # Set voltage pin 1 to output
   wpi.pinMode(V2_PIN, wpi.OUTPUT)  # Set voltage pin 2 to output
   wpi.pinMode(V3_PIN, wpi.OUTPUT)  # Set voltage pin 3 to output
   wpi.pinMode(V4_PIN, wpi.OUTPUT)  # Set voltage pin 4 to output

   wpi.pinMode(LDR_PIN1, wpi.INPUT)  # Set LDR pin 1 to input
   wpi.pinMode(LDR_PIN2, wpi.INPUT)  # Set LDR pin 2 to input
   wpi.pinMode(LDR_PIN3, wpi.INPUT)  # Set LDR pin 3 to input
   wpi.pinMode(LDR_PIN4, wpi.INPUT)  # Set LDR pin 4 to input
   wpi.pinMode(LDR_PIN5, wpi.INPUT)  # Set LDR pin 5 to input

   wpi.pinMode(LED_PIN, wpi.OUTPUT)  # Set LED pin to output

   i = 1  # Initialize variable i

   start_time = time.time()  # Record the start time
   seconds = 30  # Define a duration in seconds

   LDR_SCORE1 = 0  # Initialize LDR score 1
   LDR_SCORE2 = 0  # Initialize LDR score 2
   LDR_SCORE3 = 0  # Initialize LDR score 3
   LDR_SCORE4 = 0  # Initialize LDR score 4
   BALLS = 0  # Initialize the number of balls

   # Initialize variables for signals (button and LDR states)
   signal_old_on = 0
   signal_old_off = 0
   signal_old_L = 0
   signal_old_R = 0

   signal_new_on = 0
   signal_new_off = 0
   signal_new_L = 0
   signal_new_R = 0

   signal_new1 = 0
   signal_new2 = 0
   signal_new3 = 0
   signal_new4 = 0
   signal_new5 = 0

   signal_old1 = 0
   signal_old2 = 0
   signal_old3 = 0
   signal_old4 = 0
   signal_old5 = 0

   off = 2  # Initialize the off variable

   prev_temp = None  # Initialize prev_temp and prev_humi to None
   prev_humi = None

   def stop():
       print("Poweroff")  # Print a message to indicate power off

       # Reset global variables
       global LDR_SCORE1
       global LDR_SCORE2
       global LDR_SCORE3
       global LDR_SCORE4
       global BALLS

       LDR_SCORE1 = 0  # Reset LDR score 1
       LDR_SCORE2 = 0  # Reset LDR score 2
       LDR_SCORE3 = 0  # Reset LDR score 3
       LDR_SCORE4 = 0  # Reset LDR score 4
       BALLS = 0  # Reset the number of balls

       # Turn off voltage pins
       wpi.digitalWrite(V1_PIN, wpi.LOW)
       wpi.digitalWrite(V2_PIN, wpi.LOW)
       wpi.digitalWrite(V3_PIN, wpi.LOW)
       wpi.digitalWrite(V4_PIN, wpi.LOW)

       # Turn off laser pins
       wpi.digitalWrite(LASER_PIN1, wpi.LOW)
       wpi.digitalWrite(LASER_PIN2, wpi.LOW)
       wpi.digitalWrite(LASER_PIN3, wpi.LOW)
       wpi.digitalWrite(LASER_PIN4, wpi.LOW)
       wpi.digitalWrite(LASER_PIN5, wpi.LOW)

   def start():
       # Turn on voltage pins.
       wpi.digitalWrite(V1_PIN, wpi.HIGH)
       wpi.digitalWrite(V2_PIN, wpi.HIGH)
       wpi.digitalWrite(V3_PIN, wpi.HIGH)
       wpi.digitalWrite(V4_PIN, wpi.HIGH)
       
       # Turn on laser pins.
       wpi.digitalWrite(LASER_PIN1, wpi.HIGH)
       wpi.digitalWrite(LASER_PIN2, wpi.HIGH)
       wpi.digitalWrite(LASER_PIN3, wpi.HIGH)
       wpi.digitalWrite(LASER_PIN4, wpi.HIGH)
       wpi.digitalWrite(LASER_PIN5, wpi.HIGH)

       wpi.wiringPiSetup()

       global prev_temp
       global prev_humi

       #Read data using pin 7
       instance = DHT11(pin = 7)
       result = instance.read()

       #Check (and print) the results
       if result.is_valid():
          # print("Temperature: %-2d C" % result.temperature)
          # print("Humidity: %-2d %%" % result.humidity)
          # print(meting)

          if prev_temp is not None and prev_humi is not None: 
            current_temp = int(result.temperature)
            current_humi = int(result.humidity)

            # Round the previous values as well.
            prev_temp_int = int(prev_temp)
            prev_humi_int = int(prev_humi)
            
            # Check if the current temperature or humidity differs from the previous integer values.
            if current_temp != prev_temp_int or current_humi != prev_humi_int:
                print("Temperature: %-2d C" % current_temp)
                print("Humidity: %-2d %%" % current_humi)
                print("---------------------------------------------------------")
                time = datetime.now()
                cursor = database.cursor()
                cursor.execute("INSERT INTO tempVocht (timestamps, temperatuur, vochtigheid) VALUES ( %s, %s, %s)", (time, current_temp, current_humi))
                database.commit()

          # Check if the current temperature or humidity differs from the previous integer values.
          prev_temp = result.temperature  # Update prev_temp and prev_humi
          prev_humi = result.humidity

#       else:
#          print("Error: %d" % result.error_code)

       # Terminate the program if the temperature is above 50 or humidity is above 90.
       if result.temperature > 50 or result.humidity > 90:
          sys.exit()
       
   def servo_en_knoppen():

        time.sleep(0.05)

        # Check if the left button is pressed (state = 0).
        if wpi.digitalRead(BUTTON_PINL) == 0:
            # Set value for the left servo to neutral stance.
            servoSpinL = 250
            wpi.pwmWrite(SERVO_PINL, servoSpinL)

        # Check if the left button is not pressed (state = 1).
        elif wpi.digitalRead(BUTTON_PINL) == 1:
            # Set value for the left servo to flip stance.
            servoSpinL = 400
            wpi.pwmWrite(SERVO_PINL, servoSpinL)

        # Check if the right button is pressed (state = 0).
        if wpi.digitalRead(BUTTON_PINR) == 0:
            # Set value for the right servo to neutral stance.
            servoSpinR = 250
            wpi.pwmWrite(SERVO_PINR, servoSpinR)

        # Check if the right button is pressed (state = 1).
        if wpi.digitalRead(BUTTON_PINR) == 1:
            # Set value for the right servo to flip stance.
            servoSpinR = 100
            wpi.pwmWrite(SERVO_PINR, servoSpinR)


   def ldr_score(database):
        global i # Counter variable to determine if system is on or off.

        # Read the state of LDR sensors
        signal_new1 = wpi.digitalRead(LDR_PIN1)
        signal_new2 = wpi.digitalRead(LDR_PIN2)
        signal_new3 = wpi.digitalRead(LDR_PIN3)
        signal_new4 = wpi.digitalRead(LDR_PIN4)
        signal_new5 = wpi.digitalRead(LDR_PIN5)

        # Global variables to track the previous state of LDR sensors which is initialy 0 of all.
        global signal_old1
        global signal_old2
        global signal_old3
        global signal_old4
        global signal_old5

        # Global variables to keep track of LDR scores and BALLS. These variables are put to zero when the game is stopped now it can remember that.
        global LDR_SCORE1
        global LDR_SCORE2
        global LDR_SCORE3
        global LDR_SCORE4
        global BALLS

        # Check if LDR is triggered and was not triggered before, if so add points.
        if signal_new1 == 1 and signal_old1 == 0:
                LDR_SCORE1 += 10
                print("Score poort 10 pt:", LDR_SCORE1)
        signal_old1 = signal_new1

        if signal_new2 == 1 and signal_old2 == 0:
                LDR_SCORE2 += 20
                print("Score poort 20 pt:", LDR_SCORE2)
        signal_old2 = signal_new2

        if signal_new3 == 1 and signal_old3 == 0:
                LDR_SCORE3 += 30
                print("Score poort 30 pt:", LDR_SCORE3)
        signal_old3 = signal_new3

        if signal_new4 == 1 and signal_old4 == 0:
                LDR_SCORE4 += 40
                print("Score poort 40 pt:", LDR_SCORE4)
        signal_old4 = signal_new4

        # Check if LDR1 is triggered and was not triggered before, if so add points.
        if signal_new5 == 1 and signal_old5 == 0:
                BALLS += 1
                print(BALLS)
        signal_old5 = signal_new5

        # if two balls has passed.
        # Your total score will be displayed.
        # If the player's name is inputted, the info is put in the database. 
        # The game will stop.
        if BALLS > 2:
                TOTAAL_SCORE = LDR_SCORE1 + LDR_SCORE2 + LDR_SCORE3 + LDR_SCORE4
                print("your score is %d. ", TOTAAL_SCORE)
                name = input("What is your name?")
                time = datetime.now()
                cursor = database.cursor()
                cursor.execute("INSERT INTO score (timestamps, name, totalscore) VALUES ( %s, %s, %s)", (time, name, TOTAAL_SCORE))
                database.commit()
                BALLS = 0
                i = 1

while True:
    # Time for maximum time that's past.
    current_time = time.time()
    elapsed_time = current_time - start_time
    signal_new_off = wpi.digitalRead(BUTTON_PIN_OFF)
    signal_new_on = wpi.digitalRead(BUTTON_PIN_ON)
    signal_new_L = wpi.digitalRead(BUTTON_PINL)
    signal_new_R = wpi.digitalRead(BUTTON_PINR)
    
    
    # Reset time to elapsed = 0 if one flipper button is pressed.
    if signal_new_L == 1 and signal_old_L == 0:
        start_time = current_time
    signal_old_L = signal_new_L    

    if signal_new_R == 1 and signal_old_R == 0:
        start_time = current_time
    signal_old_R = signal_new_R

    # Stop game if stop button is pressed.
    if signal_new_off == 1 and signal_old_off == 0:
        i = 1

    # If elapsed time bigger is than given seconds (game), stop the game.
    if elapsed_time > seconds:
        i = 1

    # Stop state.
    while i > 0:
        time.sleep(0.3)
        stop()
        signal_new_off = wpi.digitalRead(BUTTON_PIN_OFF)
        start_time = current_time

        # if you press four times on the stop button a website with randomised port will open.
        if signal_new_off == 1 and signal_old_off == 0:
            i += 1
            print("stop button pressed", i)

            if i > 3:
                print("website", i)
                x = randint(4000, 9000)
                app.run(host="0.0.0.0", port=x)
                i = 1
        # Break the inner loop if the "on" button is pressed
        signal_new_on = wpi.digitalRead(BUTTON_PIN_ON)
        if signal_new_on == 1 and signal_old_on == 0:
            i = 0
            signal_old_on = signal_new_on  # Update signal_old_on
            break  # Exit the inner loop

        # Update old signals for the next iteration
        signal_old_off = signal_new_off
        signal_old_on = signal_new_on

     # Update old signals for the next iteration
    signal_old_off = signal_new_off
    signal_old_on = signal_new_on

    start()
    servo_en_knoppen()
    ldr_score(database)
