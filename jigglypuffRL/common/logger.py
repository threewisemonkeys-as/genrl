import sys

from torch.utils.tensorboard import SummaryWriter

class Logger:
    def __init__(self, logdir=None, formats=['csv']):
        self._logdir = logdir
        self._formats = formats
        self.writers = []
        for format in self.formats:
            self.writers.append(logger_registry[format](self.logdir))

    def write(self, kvs):
        for writer in self.writers:
            writer.write(kvs)

    def close(self):
        for writer in self.writers:
            writer.close()

    @property
    def logdir(self):
        return self._logdir

    @property
    def formats(self):
        return self._formats


class HumanOutputFormat:
    def __init__(self, logdir=None):
        self.file = sys.stdout

    def write(self, kvs):
        self.file.write('\n')
        for key,value in kvs.items():
            self.file.write('{}:{}\n'.format(key, value))
        self.file.write('\n')
        self.file.flush()

    def close(self):
        self.file.close()


class TensorboardLogger:
    def __init__(self, logdir):
        self.logdir = logdir
        os.makedirs(self.logdir, exist_ok=True)
        self.writer = SummaryWriter(logdir)

    def write(self, kvs):
        for key, value in kvs.items():
            self.writer.add_scalar(key, value, kvs['timestep'])

    def close(self):
        self.writer.close()


class CSVLogger:
    def __init__(self, logdir):
        self.logdir = logdir
        os.makedirs(self.logdir, exist_ok=True)
        self.file = open('{}/train.csv'.format(logdir), 'w')
        self.first = True
        self.keynames = {}

    def write(self, kvs):
        if self.first:
            for i, key in enumerate(kvs.keys()):
                self.keynames[key] = i
                self.file.write(key)
                self.file.write(',')
            self.file.write('\n')
            self.first = False

        for i, (key,value) in enumerate(kvs.items()):
            if key not in self.keynames.keys():
                raise Exception("A new value '{}' cannot be added to CSVLogger".format(key))
            if i!=self.keynames[key]:
                raise Exception("Value not at the same index as when initialized")
            self.file.write(str(value))
            self.file.write(',')

        self.file.write('\n')

    def close(self):
        self.file.close()

logger_registry = {'stdout':HumanOutputFormat, 
                   'tensorboard':TensorboardLogger, 
                   'csv':CSVLogger}