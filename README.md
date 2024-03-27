# README.md
This is a fork of https://github.com/lolouk44/xiaomi_mi_scale/blob/master/README.md. It simply adds the ability to output the json file with all entries and run a jupyter notebook to visualize these metrics any time a new weight is added.


Sample Docker Compose

```yml
  mi-scale:
    image: leolabtech/mi-scale:latest
    container_name: mi-scale
    restart: always
    network_mode: host
    privileged: true
    volumes:
      - /var/run/dbus/:/var/run/dbus/:ro # needed for bleak
      - ./volumes/scale/data:/opt/miscale/data # must contain options.json
      - ./volumes/scale/input:/opt/miscale/input # must contain jupyter notebook named 'notebook.ipynb' and file called 'weight.json'
      - ./volumes/scale/output:/opt/miscale/output # Will contain rendered jupyter notebook in selected format(s)
    environment:
      - PUID=${PUID}
      - PGID=${PGID}
      - TZ=${TZ}
      - FORMATS=PDF,HTML,MARKDOWN # formats (comma separated)
```