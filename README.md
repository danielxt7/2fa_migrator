# **2fa_migrator**

A small utility I wrote to help me migrate my Android 2FA accounts DB (from Google Authenticator) to iOS.

## Usage


```plain
Usage: 2fa_migrator.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate  Generate QR Codes for 2FA database entries
  pull      Pull 2FA database file from your device  
```


## Example

```shell
(2famigrator)~/p/2fa_migrator ❯❯❯ ./2fa_migrator.py pull --type GA --dest ga_db.sqlite
pulling db of type 'GA' => ga_db.sqlite
executing 'adb pull /data/data/com.google.android.apps.authenticator2/databases/databases ga_db.sqlite', output:
548 KB/s (6144 bytes in 0.010s)


done.
```

Now you should have ga_db.sqlite in your CWD, use the generate command to make QR codes out of it:

```shell
(2famigrator)~/p/2fa_migrator ❯❯❯ ./2fa_migrator.py generate --type GA --db ga_db.sqlite                                                                    
writing QR Code for 'Google' => Google.png
writing QR Code for 'Facebook' => Facebook.png
writing QR Code for 'Slack' => Slack.png
...
```

Open *.png and start scanning on your device! :)
