from beets.plugins import BeetsPlugin
from beets.util import command_output, displayable_path, par_map
from beets.dbcore import types
from beets import ui
import os


class DynamicRange(BeetsPlugin):
    item_types = {
        'dr': types.INTEGER,
        'dr_peak_dB': types.Float(6),
        'dr_rms_dB': types.Float(6),
    }

    album_types = {
        'dr_min': types.INTEGER,
        'dr_max': types.INTEGER,
        'dr_avg': types.INTEGER,
    }

    def __init__(self):
        super().__init__()

        self.config.add({
            'auto': True,
            'command': 'dr14_tmeter',
        })

        if self.config['auto']:
            self.register_listener('item_imported', self.item_imported)
            self.register_listener('album_imported', self.album_imported)

    def item_imported(self, lib, item):
        self.handle_item(item)

    def album_imported(self, lib, album):
        self.handle_album(album)

    def commands(self):
        dr_command = ui.Subcommand('dr', help="compute dynamic range of music")
        dr_command.parser.add_album_option()
        dr_command.parser.add_option(
            '-f', '--force', action='store_true', default=False, dest='force',
            help='recompute dynamic range data even if present')

        dr_command.func = self.command
        return [dr_command]

    def command(self, lib, opts, args):
        if opts.album:
            albums = lib.albums(ui.decargs(args))
            self._log.info("Analyzing {} albums".format(len(albums)))

            for album in albums:
                self.handle_album(album, opts.force)
        else:
            items = lib.items(ui.decargs(args))
            self._log.info("Analyzing {} tracks".format(len(items)))

            par_map(lambda item: self.handle_item(item, opts.force), items)

    def compute_track_dr(self, file):
        cmd = [self.config['command'].as_str(), '-f', file]
        lines = command_output(cmd).stdout.decode('utf-8').split('\n')
        for line in lines:
            if line.startswith('DR'):
                dr = int(line.split('=')[1])
            elif line.startswith('Peak dB'):
                peak = float(line.split('=')[1])
            elif line.startswith('Rms dB'):
                rms = float(line.split('=')[1])
        return (dr, peak, rms)

    def item_requires_dr(self, item):
        return not all([hasattr(item, k) for k in self.item_types.keys()])

    def handle_item(self, item, force=False):
        if self.item_requires_dr(item) or force:
            dpath = displayable_path(item.path)
            if not os.path.exists(item.path):
                self._log.error(f"{dpath} does not exist!")
                return

            try:
                dr, peak, rms = self.compute_track_dr(item.path)
            except Exception as e:
                self._log.error("error computing dynamic range: {}", str(e))
                return

            item['dr'] = dr
            item['dr_peak_dB'] = peak
            item['dr_rms_dB'] = rms
            item.store()

    def album_requires_dr(self, album):
        return not all([hasattr(album, k) for k in self.album_types.keys()])

    def handle_album(self, album, force=False):
        if self.album_requires_dr(album) or force:
            items = album.items()
            par_map(lambda item: self.handle_item(item, force), items)

            drs = [item['dr'] for item in items]
            album['dr_min'] = min(drs)
            album['dr_max'] = max(drs)
            album['dr_avg'] = int(round(sum(drs) / len(drs)))
            album.store()
