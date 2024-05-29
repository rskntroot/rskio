# Example

## This is an Example Markdown File

### sphinx-docs

Sphinx Docs can be described as "website as code" similar to "infrastructure as code".

Currently, this site is built out with the following components:

```
docker: 
  img: python:alpine 
os:
  apk: py3-sphinx
python:
  pip: 
    - myst-parser
    - pydata-sphinx-theme
``` 

Sphinx is used generate the html for site which can then be hosted separately:

Generate Command:
```
make html
```

Hosting:
```
docker:
  img: nginx:latest 
```

#### Testing

```
cd /opt/docker
docker run -it --rm -v ./docs/build/html:/opt/sphinx/html/:ro -v ./nginx/etc/conf.d/:/etc/nginx/conf.d/:ro -p 9999:80 nginx:latest
``` 
