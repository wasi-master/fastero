|Snippet Code|Snippet Name|Runs|Mean|Median|Min|Max|Standard Deviation|
|---|---|---|---|---|---|---|---|
|urllib.request.urlopen(URL)|urllib|25|1.475 s|1.376 s|1.287 s|2.304 s|259.79 ms|
|urllib3.PoolManager().request("GET", URL)|urllib3|25|2.393 s|2.304 s|2.104 s|3.187 s|259.69 ms|
|requests.get(URL)|requests|25|2.295 s|2.193 s|2.037 s|2.906 s|223.47 ms|
|httpx.get(URL)|httpx|25|2.201 s|2.168 s|2.08 s|2.424 s|104.43 ms|
