
import os
import subprocess as sbp
from mutmap.utils import time_stamp
from mutmap.utils import clean_cmd
from mutmap.alignment import Alignment


class Trim(object):

    def __init__(self, args):
        self.out = args.out
        self.args = args
        self.trim_params = self.params_parser(args.trim_params)

    def params_parser(self, trim_params):
        params_list = trim_params.split(',')
        trim_params = {}
        trim_params['phred'] = params_list[0]
        trim_params['ILLUMINACLIP'] = params_list[1]
        trim_params['LEADING'] = params_list[2]
        trim_params['TRAILING'] = params_list[3]
        trim_params['SLIDINGWINDOW'] = params_list[4]
        trim_params['MINLEN'] = params_list[5]
        return trim_params

    def run(self, fastq1, fastq2, index):
        print(time_stamp(),
        'start trimming for {} and {}.'.format(fastq1, fastq2),
        flush=True)

        trim1 = '{}/00_fastq/{}.1.trim.fastq.gz'.format(self.out,
                                                        index)
        trim2 = '{}/00_fastq/{}.2.trim.fastq.gz'.format(self.out,
                                                        index)
        unpaired1 = '{}/00_fastq/{}.1.unpaired.fastq.gz'.format(self.out,
                                                                index)
        unpaired2 = '{}/00_fastq/{}.2.unpaired.fastq.gz'.format(self.out,
                                                                index)

        cmd = 'trimmomatic PE -threads {} \
                              -phred{} {} {} {} {} {} {} \
                              ILLUMINACLIP:{} \
                              LEADING:{} \
                              TRAILING:{} \
                              SLIDINGWINDOW:{} \
                              MINLEN:{} \
                              &>> {}/log/trimmomatic.log'.format(self.args.threads,
                                                                 self.trim_params['phred'],
                                                                 fastq1,
                                                                 fastq2,
                                                                 trim1,
                                                                 unpaired1,
                                                                 trim2,
                                                                 unpaired2,
                                                                 self.trim_params['ILLUMINACLIP'],
                                                                 self.trim_params['LEADING'],
                                                                 self.trim_params['TRAILING'],
                                                                 self.trim_params['SLIDINGWINDOW'],
                                                                 self.trim_params['MINLEN'],
                                                                 self.out)
        cmd = clean_cmd(cmd)
        sbp.run(cmd, stdout=sbp.DEVNULL, stderr=sbp.DEVNULL, shell=True, check=True)

        print(time_stamp(),
              'trimming for {} and {} successfully finished.'.format(fastq1, fastq2),
              flush=True)

        aln = Alignment(self.args)
        aln.run(trim1, trim2, index)
