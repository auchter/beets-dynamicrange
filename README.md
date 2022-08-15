# beets-dynamicrange

This is a [beets](https://github.com/beetbox/beets) plugin which computes the
dynamic range of your music and stores this information in the beets database.

[DR14 T.meter](https://github.com/simon-r/dr14_t.meter) is used under the hood
for the dynamic range calcuation.

## Installation

Sync this repo, and add the path to its `beetsplug` directory to your
`pluginpath`, then add `dynamicrange` to your list of plugins.

## Configuration

Two configuration options are available:

- `auto` whether to compute and store the dynamic range information during import
- `command` the command to invoke to run DR14 T.meter

The default configuration is:

```
dynamicrange:
  auto: True
  command: dr14_tmeter
```

## Usage

Running `beet dr` will compute the dynamic range for the selected items (or all
items by default). The following fields will be stored for each track:

- `dr`, the DR as reported by DR14 T.meter
- `dr_peak_dB`, the peak dB as reported by DR14 T.meter
- `dr_rms_dB`, the RMS dB as reported by DR14 T.meter

Running `beet dr -a` will additionally add the following fields to the selected
albums (or all by default):

- `dr_min`, the minimum track DR for the album
- `dr_max`, the maximum track DR for the album
- `dr_avg`, the average track DR for the album


## References

- [Dynamic Range DB](https://dr.loudness-war.info/)
