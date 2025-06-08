#include <stdint.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "nvs_flash.h"

#include "esp_bt.h"
#include "esp_gap_ble_api.h"
#include "esp_gattc_api.h"
#include "esp_gatt_defs.h"
#include "esp_bt_main.h"
#include "esp_bt_defs.h"
#include "esp_log.h"
#include "esp_mac.h"

#include "esp_sleep.h"

#define DELAY_IN_S 30

static const char* LOG_TAG = "esp32-tag";

/** Callback function for BT events */
static void esp_gap_cb(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param);

/** Random device address */
static esp_bd_addr_t rnd_addr = { 0xFF, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF };

/** Advertisement payloads */
static uint8_t adv_data_apple[31] = {
	0x1e, /* Length (30) */
	0xff, /* Manufacturer Specific Data (type 0xff) */
	0x4c, 0x00, /* Company ID (Apple) */
	0x12, 0x19, /* Offline Finding type and length */
	0x00, /* State */
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, /* First two bits */
	0x00, /* Hint (0x00) */
};

static uint8_t adv_data_google[31] = {
    0x02,   // Length
    0x01,   // Flags data type value
    0x06,   // Flags data
    0x19,   // Length
    0x16,   // Service data data type value
    0xAA,   // 16-bit service UUID
    0xFE,   // 16-bit service UUID
    0x41,   // FMDN frame type with unwanted tracking protection mode indication
            // 20-byte ephemeral identifier (inserted below)
            // Hashed flags (implicitly initialized to 0)
};

typedef struct {
    uint8_t type;
    uint8_t public_key[28];
} advertising_key_t;

// 0x00 - Apple
// 0x01 - Google
static advertising_key_t advertising_keys[] = {
    {0x00, {0xaa, 0xbb, 0xcc, 0xdd, 0xee}},
    {0x01, {0xaa, 0xbb, 0xcc, 0xdd, 0xee}}
};

/* https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/esp_gap_ble.html#_CPPv420esp_ble_adv_params_t */
static esp_ble_adv_params_t ble_adv_params = {
    // Advertising min interval:
    // Minimum advertising interval for undirected and low duty cycle
    // directed advertising. Range: 0x0020 to 0x4000 Default: N = 0x0800
    // (1.28 second) Time = N * 0.625 msec Time Range: 20 ms to 10.24 sec
    .adv_int_min        = 0x0020, 
    // Advertising max interval:
    // Maximum advertising interval for undirected and low duty cycle
    // directed advertising. Range: 0x0020 to 0x4000 Default: N = 0x0800
    // (1.28 second) Time = N * 0.625 msec Time Range: 20 ms to 10.24 sec
    .adv_int_max        = 0x0020,
    // Advertisement type
    .adv_type           = ADV_TYPE_NONCONN_IND,
    // Use the random address
    .own_addr_type      = BLE_ADDR_TYPE_RANDOM,
    // All channels
    .channel_map        = ADV_CHNL_ALL,
    // Allow both scan and connection requests from anyone. 
    .adv_filter_policy = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,
};
static void esp_gap_cb(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param)
{
    esp_err_t err;

    switch (event) {
        case ESP_GAP_BLE_ADV_DATA_RAW_SET_COMPLETE_EVT:
            esp_ble_gap_start_advertising(&ble_adv_params);
            break;

        case ESP_GAP_BLE_ADV_START_COMPLETE_EVT:
            //adv start complete event to indicate adv start successfully or failed
            if ((err = param->adv_start_cmpl.status) != ESP_BT_STATUS_SUCCESS) {
                ESP_LOGE(LOG_TAG, "advertising start failed: %s", esp_err_to_name(err));
            } else {
                ESP_LOGI(LOG_TAG, "advertising has started.");
            }
            break;

        case ESP_GAP_BLE_ADV_STOP_COMPLETE_EVT:
            if ((err = param->adv_stop_cmpl.status) != ESP_BT_STATUS_SUCCESS){
                ESP_LOGE(LOG_TAG, "adv stop failed: %s", esp_err_to_name(err));
            }
            else {
                ESP_LOGI(LOG_TAG, "stop adv successfully");
            }
            break;
        default:
            break;
    }
}

void set_addr_from_key(esp_bd_addr_t addr, uint8_t *public_key) {
	addr[0] = public_key[0] | 0b11000000;
	addr[1] = public_key[1];
	addr[2] = public_key[2];
	addr[3] = public_key[3];
	addr[4] = public_key[4];
	addr[5] = public_key[5];
}

void set_payload_from_apple_key(uint8_t *payload, uint8_t *public_key) {
    /* copy last 22 bytes */
	memcpy(&payload[7], &public_key[6], 22);
	/* append two bits of public key */
	payload[29] = public_key[0] >> 6;
}

void set_payload_from_google_key(uint8_t *payload, uint8_t *public_key) {
    memcpy(&payload[8], public_key, 20);
}

void disable_bt_task(void *arg) {
    ESP_LOGI(LOG_TAG, "Disabling BT");

    esp_bluedroid_disable();
    esp_bluedroid_deinit();

    esp_bt_controller_disable();
    esp_bt_controller_deinit();

    ESP_LOGI(LOG_TAG, "BT disabled");
    vTaskDelay(10);
    vTaskDelete(NULL);
}

void enable_bt_task(void *arg) {
    ESP_LOGI(LOG_TAG, "Enabling BT");

    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    esp_bt_controller_init(&bt_cfg);
    esp_bt_controller_enable(ESP_BT_MODE_BLE);

    esp_bluedroid_config_t bluedroid_cfg = BT_BLUEDROID_INIT_CONFIG_DEFAULT();
    esp_bluedroid_init_with_cfg(&bluedroid_cfg);
    esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_ADV, ESP_PWR_LVL_P20);
    esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_DEFAULT, ESP_PWR_LVL_P20);
    esp_bluedroid_enable();

    ESP_LOGI(LOG_TAG, "BT enabled");
    vTaskDelay(10);
    vTaskDelete(NULL);
}

void app_main(void)
{
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));
    xTaskCreate(&enable_bt_task, "bt_enable", 4096, NULL, 5, NULL);

    ESP_LOGI(LOG_TAG, "application initialized");

    esp_err_t status;
        if ((status = esp_ble_gap_register_callback(esp_gap_cb)) != ESP_OK) {
            ESP_LOGE(LOG_TAG, "gap register error: %s", esp_err_to_name(status));
            return;
        }

    int key_index = 0;
    while(true) {
        esp_err_t status;
        advertising_key_t key;
        uint8_t* adv_data;
        uint32_t adv_data_len;

        if ((status = esp_ble_gap_clear_advertising()) != ESP_OK) {
            ESP_LOGE(LOG_TAG, "clear data error: %s", esp_err_to_name(status));
            return;
        }
        vTaskDelay(10);
        if ((status = esp_ble_gap_clear_rand_addr()) != ESP_OK) {
            ESP_LOGE(LOG_TAG, "clear adress error: %s", esp_err_to_name(status));
            return;
        }
        vTaskDelay(10);

	    key = advertising_keys[key_index];
        if (key.type == 0x00) {
            ESP_LOGI(LOG_TAG, "using apple network");

            
            ble_adv_params.own_addr_type = BLE_ADDR_TYPE_RANDOM;

            set_addr_from_key(rnd_addr, key.public_key);
            set_payload_from_apple_key(adv_data_apple, key.public_key);

            adv_data = adv_data_apple;
            adv_data_len = sizeof(adv_data_apple);
            ESP_LOGI(LOG_TAG, "using random address: %02X:%02X:%02X:%02X:%02X:%02X", rnd_addr[0], rnd_addr[1], rnd_addr[2], rnd_addr[3], rnd_addr[4], rnd_addr[5]);
        } else if (key.type == 0x01) {
            ESP_LOGI(LOG_TAG, "using google network");


            ble_adv_params.own_addr_type = BLE_ADDR_TYPE_PUBLIC;

            uint8_t mac_addr[6];
            uint8_t mac_addr_type[2];

            esp_ble_gap_get_local_used_addr(mac_addr, mac_addr_type);
            set_payload_from_google_key(adv_data_google, key.public_key);

            adv_data = adv_data_google;
            adv_data_len = sizeof(adv_data_google);
            ESP_LOGI(LOG_TAG, "using device address: %02X:%02X:%02X:%02X:%02X:%02X", mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
        } else {
            ESP_LOGE(LOG_TAG, "invalid key type");
            key_index = (key_index + 1) % (sizeof(advertising_keys)/sizeof(advertising_keys[0]));
            continue;
        }
        
        if (key.type == 0x00) {
            if ((status = esp_ble_gap_set_rand_addr(rnd_addr)) != ESP_OK) {
            ESP_LOGE(LOG_TAG, "couldn't set random address: %s", esp_err_to_name(status));
            return;
            }
            vTaskDelay(10);
        }
    
        if ((esp_ble_gap_config_adv_data_raw(adv_data, adv_data_len)) != ESP_OK) {
            ESP_LOGE(LOG_TAG, "couldn't configure BLE adv: %s", esp_err_to_name(status));
            return;
        }
        
	    ESP_LOGI(LOG_TAG, "Sending beacon (with key index %d)", key_index);
        vTaskDelay(100);
	    esp_ble_gap_stop_advertising();
	    vTaskDelay(10);

        // Light sleep technique (Uses less power but less stable light sleeping not works with bluetooth)
        // Disable bluetooth
        xTaskCreate(&disable_bt_task, "bt_disable", 4096, NULL, 5, NULL);
        vTaskDelay(10);
        ESP_LOGI(LOG_TAG, "Going to sleep");
        vTaskDelay(10);

        esp_sleep_enable_timer_wakeup(DELAY_IN_S * 1000000);
        esp_light_sleep_start();

        ESP_LOGI(LOG_TAG, "Returned from light sleep");
        vTaskDelay(10);

        // Re-enable bluetooth
        xTaskCreate(&enable_bt_task, "bt_enable", 4096, NULL, 5, NULL);
        vTaskDelay(10);

        // Normal sleeping technique (Uses more power but more stable)
        //vTaskDelay(DELAY_IN_S * 100);

	    key_index = (key_index + 1) % (sizeof(advertising_keys)/sizeof(advertising_keys[0]));
    }   
}