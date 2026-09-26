/*
 * board.h - LPC1114-LCD rev 1.0 pin map and board constants.
 *
 * Generated from the hardware design (hardware/LPC1114-LCD.kicad_sch).
 * Keep in sync with the schematic whenever the hardware changes.
 */
#ifndef BOARD_H
#define BOARD_H

/* ---------------------------------------------------------------- Clocks */
#define BOARD_XTAL_HZ           12000000UL  /* Y1, system oscillator (XTALIN/XTALOUT) */
#define BOARD_CORE_CLOCK_HZ     48000000UL  /* 12 MHz x 4 via system PLL */

/* ---------------------------------------------------------------- Pin convention
 * Each signal is described by its GPIO port (0/1) and bit number.
 * NOTE: PIO0_11, PIO1_0, PIO1_1 and PIO1_2 start in a reserved function after
 * reset: their IOCON register must select FUNC = 1 (GPIO) and digital mode (ADMODE = 1).
 */

/* ---------------------------------------------------------------- LCD 1602 (4-bit, write only: R/W tied to GND)
 * Lines are 5 V tolerant; RN1 pulls them to 5 V so the firmware may use either
 * push-pull (3.3 V high) or open-drain (IOCON OD = 1, 5 V high via RN1).
 */
#define LCD_RS_PORT             1
#define LCD_RS_PIN              5   /* PIO1_5, DIP pin 14 */
#define LCD_E_PORT              1
#define LCD_E_PIN               4   /* PIO1_4, DIP pin 13 */
#define LCD_D4_PORT             1
#define LCD_D4_PIN              2   /* PIO1_2, DIP pin 11 (IOCON FUNC=1) */
#define LCD_D5_PORT             1
#define LCD_D5_PIN              1   /* PIO1_1, DIP pin 10 (IOCON FUNC=1) */
#define LCD_D6_PORT             1
#define LCD_D6_PIN              0   /* PIO1_0, DIP pin 9  (IOCON FUNC=1) */
#define LCD_D7_PORT             0
#define LCD_D7_PIN              6   /* PIO0_6, DIP pin 6 */

/* Backlight: NPN low-side switch, active high. PWM on CT32B0_MAT3 (IOCON FUNC=3). */
#define LCD_BL_PORT             0
#define LCD_BL_PIN              11  /* PIO0_11, DIP pin 4 (IOCON FUNC=1 for GPIO) */

/* ---------------------------------------------------------------- Buttons (active low, 10k external pull-ups) */
#define BTN_MODE_PORT           0
#define BTN_MODE_PIN            1   /* PIO0_1, DIP pin 24 - held low at reset = UART ISP */
#define BTN_UP_PORT             0
#define BTN_UP_PIN              9   /* PIO0_9, DIP pin 2 */
#define BTN_DOWN_PORT           1
#define BTN_DOWN_PIN            8   /* PIO1_8, DIP pin 17 */
#define BTN_OK_PORT             0
#define BTN_OK_PIN              8   /* PIO0_8, DIP pin 1 */

/* ---------------------------------------------------------------- LEDs (active high, 470R) */
#define LED1_PORT               0
#define LED1_PIN                2   /* PIO0_2, DIP pin 25 - red */
#define LED2_PORT               0
#define LED2_PIN                3   /* PIO0_3, DIP pin 26 - yellow */
#define LED3_PORT               0
#define LED3_PIN                7   /* PIO0_7, DIP pin 28 - green (high-current pin) */

/* ---------------------------------------------------------------- Buzzer (passive, NPN driver, active high)
 * PWM on CT16B1_MAT0 (IOCON FUNC=1). 10k pull-down keeps it off during reset.
 */
#define BUZZER_PORT             1
#define BUZZER_PIN              9   /* PIO1_9, DIP pin 18 */

/* ---------------------------------------------------------------- I2C: DS3231M RTC (4k7 pull-ups to 3.3 V) */
#define I2C_SCL_PORT            0
#define I2C_SCL_PIN             4   /* PIO0_4, DIP pin 27 */
#define I2C_SDA_PORT            0
#define I2C_SDA_PIN             5   /* PIO0_5, DIP pin 5 */
#define RTC_I2C_ADDR            0x68U

/* ---------------------------------------------------------------- UART (CH340C on micro USB, and header J3) */
#define UART_RXD_PORT           1
#define UART_RXD_PIN            6   /* PIO1_6, DIP pin 15 */
#define UART_TXD_PORT           1
#define UART_TXD_PIN            7   /* PIO1_7, DIP pin 16 */
#define UART_DEFAULT_BAUD       115200UL

#endif /* BOARD_H */
