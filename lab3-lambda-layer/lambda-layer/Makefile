BASE_NAME=ffmpeg
DEPLOYMENT_BUCKET_NAME := wolfeste-hd-lambda-thumbnail
DEPLOYMENT_KEY := resources/aws-ffmpeg-serverless-convert/$(shell echo $(BASE_NAME)-$$RANDOM.zip)
STACK_NAME := $(BASE_NAME)-lambda-layer

clean:
	rm -rf build

build/bin/ffmpeg:
	mkdir -p build/bin
	rm -rf build/ffmpeg*
	cd build; \
		curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ
	mv build/ffmpeg*/ffmpeg build/ffmpeg*/ffprobe build/bin

build/layer.zip: build/bin/ffmpeg
	cd build && zip -r layer.zip bin

build/output.yml: build/layer.zip

deploy: build/output.yml
	aws s3 cp build/layer.zip s3://$(DEPLOYMENT_BUCKET_NAME)/$(DEPLOYMENT_KEY)