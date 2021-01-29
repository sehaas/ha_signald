# Signal Notifications

Sending Signal notification using the [signald daemon](https://gitlab.com/signald/signald)

## Config

| Config    | Requires | Default               | Comment                                 |
| --------- | -------- | --------------------- | --------------------------------------- |
| sender_nr | yes      |                       | phone number of registered signald user |
| recp_nr   | no       |                       | phone number of recipient               |
| group     | no       |                       | base64 hash of group ID                 |
| socket    | no       | /signald/signald.sock | UNIX socket of signald daemon           |

Either `recp_nr` or `group` must be configured. If both are configured `recp_nr` will be ignored.
How to setup `signald` is out of scope of this document, but can be found [here](https://gitlab.com/signald/signald/-/blob/main/README.md).

### Example

send to singe recipient
```
notify:
  - name: send_to_joe
    platform: signald
    sender_nr: '+431112223333'
    recp_nr: '+431112224444'
```
send to group
```
notify:
  - name: group_message
    platform: signald
    sender_nr: '+431112223333'
    group: 'UVW01hfCIPS/1ITwhhHF1QYln1HG4mRqnLBkE5+HDUo='
```
use custom socket path
```
notify:
  - name: send_to_joe
    platform: signald
    sender_nr: '+43111222555'
    recp_nr: '+431112224444'
    socket: '/custom/signald.sock'
```

## Sending messages

The additionally to the required `message` you can attach multiple attachments.
The `signald` daemon needs filesystem access to the attachment files.

### Example
```
message: 'Hello World!'
data:
  attachments:
    - '/tmp/cool_cat.gif'
    - '/data/IMG_2021.jpg'
```
