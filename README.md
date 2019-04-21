Information
---

##### Description

 - 監控寶告警Webhook

##### Run Service
 - python3 guardian-bao.py
 

Configure File
---

##### file name
 - guardian.conf

##### [Teamplus]
 
 - api_url - TeamPlus API URL
 - account - TeamPlus 帳號名稱
 - api_key - TeamPlus 帳號的API Key
 - chat_sn - TeamPlus 聊天室編號

 
##### [JiankongbaoAlert]

 - api_port - 服務Port
 - api_token - 於監控寶上面服務的port
 - prefix - 推播teamplus訊息的前綴
