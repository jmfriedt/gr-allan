Convert the provided ASCII file to binary to be read by GNU Radio:
```bash
cat noisetest.ykt  | grep -v ^% | cut -c29-51 | tr "\n" " " | ascii2binary -tf > t
```
