1. Connection

 

     Mifare_RC522_RFID  OP One

     MOSI â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”> pin 19

     MISO â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”-> pin 21

     SCLK â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”-> pin 23

     SDA â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€“> pin 24

     RST â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”> pin 22

     IRQ â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”â€”-> NONE

 

2. Check device ls /dev/spidev0.0 ( Armbian 5.04 gives it out of the box)

 

3) Install python dev

    apt-get install python-dev
    apt-get install python3-dev
     python-dev-is-python3

 

4) Install orangepi_PC_gpio_pyH3 Library

      git clone https://github.com/duxingkei33/orangepi_PC_gpio_pyH3.git

      cd orangepi_PC_gpio_pyH3

      python setup.py install

sudo apt update
sudo apt upgrade
sudo apt install -y git 
git clone https://github.com/orangepi-xunlong/wiringOP.git -b next
cd wiringOP
sudo ./build clean
sudo ./build
echo "BOARD=orangepi5plus" | sudo tee /etc/orangepi-release
gpio readall


git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
sudo python setup.py install

pip install python3-spi


git clone https://github.com/mxgxw/MFRC522-python.git
cd MFRC522-python

5) Install SPI-Py Library

    git clone https://github.com/lthiery/SPI-Py.git

    cd SPI-Py

     python setup.py install

 

6) Install MFRC522-python

     git clone https://github.com/rasplay/MFRC522-python.git

 

7)To read id data:

    cd MFRC522-python

    edit  MFRC522.py and comment out line 108.109.110  and 356( as shown below)

          # GPIO.setmode(GPIO.BOARD)

          #GPIO.setup(22, GPIO.OUT)

          #GPIO.output(self.NRSTPD, 1)

    

           #GPIO.output(self.NRSTPD, 1)

 

        python read.py

 

root@orangepione:~/MFRC522-python# python read.py

Card read UID: 193,11,21,149,74