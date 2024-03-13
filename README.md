~~It's a very simple implement. No framework. Just run 「python main.py」~~
Now you can invok web server via curl.
```
curl --location 'http://127.0.0.1:8000/check_updates/?app_name=AFFiNE'

「app_name」is a optinal param.

JSON RESULT

[
  {
    "app_name": "AFFiNE",
    "current_version": "0.12.1",
    "latest_version": "0.12.2",
    "update_required": true,
    "download_url": "https://objects.githubusercontent.com/github-production-release-asset-2e65be/519859998/ad5f292e-9c9b-4c64-bae3-af5bba925702?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-    Credential=AKIAVCODYLSA53PQK4ZA%2F20240313%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240313T095055Z&X-Amz-Expires=300&X-Amz-Signature=3505fd0db7fd47dc16b407adf92a97ee881b44fc08a5ded7e073753fe6eefa52&X-Amz-  SignedHeaders=host&actor_id=0&key_id=0&repo_id=519859998&response-content-disposition=attachment%3B%20filename%3Daffine-stable-macos-arm64.zip&response-content-type=application%2Foctet-stream"
  }
]
```

You can see the support apps in config folder.If u want to check more AppStore APPs, just edit config/app_to_link_mapping_appstore.json file

Key is App name, value is the APP Store Link!

I wrote this project because I always love checking apps for updates.

