# DataDog agent v6 with Google Pagespeed Insight checks

## What is this?

A check module written in python that can be used in the DataDog agent (https://www.datadoghq.com/).
The module runs periodic checks via Google Pagespeed Insights API against the configured URL and sends
metrics to DataDog.

## Configuration

Check the `manifest/etc/datadog-agent/conf.d/pagespeed.yaml`.

```
init_config:
  google_api_key: your-api-key
  # number of seconds to get response for pagespeed API
  timeout: 30

instances:
  - url: http://www.example.com
    min_collection_interval: 3600
    tags:
      - env:prod
      - page_family:home
      - page:home

  - url: http://staging.example.com/microsite
    min_collection_interval: 3600
    tags:
      - env:staging
      - page_family:home
      - page:microsite
```

You can configure multiple URLs, each with its own checking interval.
You can defined tags for the metrics. The check will automatically add tags for strategy and URL.

You can create an API key for PageSpeed API at https://console.developers.google.com/apis/credentials

## Collected metrics

 - speed score (`pagespeed.score`)
 - median first contentful paint (ms) (`pagespeed.median_fcp`)
 - median DOM content loaded event fired (ms) (`pagespeed.median_dcl`)
 - numberResources  (`pagespeed.numberResources`)
 - numberHosts (`pagespeed.numberHosts`)
 - totalRequestBytes (`pagespeed.totalRequestBytes`)
 - numberStaticResources (`pagespeed.numberStaticResources`)
 - htmlResponseBytes (`pagespeed.htmlResponseBytes`)
 - overTheWireResponseBytes (`pagespeed.overTheWireResponseBytes`)
 - cssResponseBytes (`pagespeed.cssResponseBytes`)
 - imageResponseBytes (`pagespeed.imageResponseBytes`)
 - javascriptResponseBytes (`pagespeed.javascriptResponseBytes`)
 - otherResponseBytes (`pagespeed.otherResponseBytes`)
 - numberJsResources (`pagespeed.numberJsResources`)
 - numberCssResources (`pagespeed.numberCssResources`)
 - numTotalRoundTrips (`pagespeed.numTotalRoundTrips`)
 - numRenderBlockingRoundTrips (`pagespeed.numRenderBlockingRoundTrips`)

For detailed description please see: https://developers.google.com/speed/docs/insights/v4/reference/pagespeedapi/runpagespeed

## How to use it

You can build this docker image and use it as you would use the official DataDog docker image (https://hub.docker.com/r/datadog/agent/) or you can just copy the module file and configuration to your own DataDog Agent docker image and extends as you wish.

```
docker build --tag <your-dd-agent:tag> .

docker run -d -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -e DD_API_KEY=<YOUR_API_KEY> \
              <your-dd-agent:tag>
```
