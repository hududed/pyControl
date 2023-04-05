from threading import Thread

#Change this to motion_thread
class MotionThread(Thread):
   
    def run(self):
        import pandas as pd
        d = pd.read_csv('foreward.trj',header=None) # scantime 2 (see segment 1 or row1)
        d = d.loc[:, (d != 0).any(axis=0)] # remove last 3 cols with 0
        d.columns = ['ramptime','rampdist','rampvel']
        total_time=np.sum(d['ramptime'])
        
        if d['ramptime'][0]<0.5:
            time.sleep(.5-d['ramptime'][0])
        print("MOTION THREAD\n")
        print("XPS run trajectory")
        xps.run_trajectory('foreward',)
        print('Total time {} in class'.format(total_time))
        time.sleep(total_time)
        print("TOTAL_TIME DONE, LASER 0.05W")
        laser_power.power=0.01
        print("finished and current position is:\n")
        pos_all()

#Change this to mirror_thread
class MirrorThread(Thread):
    """MOTOR THREAD"""
    def run(self):
        import pandas as pd
        d = pd.read_csv('foreward.trj',header=None) # scantime 2 (see segment 1 or row1)
        d = d.loc[:, (d != 0).any(axis=0)] # remove last 3 cols with 0
        d.columns = ['ramptime','rampdist','rampvel']
        mirror_sleep=d['ramptime'][0]-.5
        print("MIRROR THREAD")
        for i in range(2):
            if i==0:
                print(d['ramptime'][0])
                if d['ramptime'][0]<0.5:
                    print("mirror on")
       
                    start_time = time.monotonic()
                    mirror('on')
       
                    end_time = time.monotonic()
                    print(timedelta(seconds=end_time - start_time))
                    time.sleep(d['ramptime'][1]) #time for linear line    

                else:
                    print('{} > 0.5'.format(d['ramptime'][0]))
                    print('Mirror sleep {} in class'.format(mirror_sleep))
                    time.sleep(mirror_sleep)
                
                    print("mirror on")
                    start_time = time.monotonic()
                    mirror('on')
                    end_time = time.monotonic()
                    print(timedelta(seconds=end_time - start_time))
                    time.sleep(d['ramptime'][1]) #time for linear line
            else:
                mirror('off')
                print("mirror off")