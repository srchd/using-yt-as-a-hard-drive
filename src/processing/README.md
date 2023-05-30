## how to use

#### test files
I used the following files:

 - constitution of the Weimar Republic: https://germanhistorydocs.ghi-dc.org/pdf/eng/ghi_wr_weimarconstitution_Eng.pdf
 - base video: https://www.youtube.com/watch?v=dQw4w9WgXcQ

#### test parameters
These scripts have only been tested with these parameters (`patch_height = 8`, `patch_width = 8`, `rep = 10`), you can experiment, but you might run into bugs.

#### encode file in video 
```
python -m src.processing.encode -f weimar.pdf -o weimar.mp4 -v rick.mp4 --temp_path tmp --settings_file weimar.json --repetitions 10 --patch_height 8 --patch_width 8
```  
This script also creates a .json where the patch dimensions, repetition count and tail of the binary are stored. You should read them and provide them to the decoding script. These could be stored in the video description for example.

#### decoding
after uploading the generated video to youtube and downloading it again, you can decode the video like this:  
```
python -m src.processing.decode -v 'Glitched Up White Boy.mp4' -o weimar_reconstructed.pdf --tail_size 704 --patch_height 8 --patch_width 8 --repetitions 10
```  
**NOTE**: trying to decode an encoded video without uploading-downloading will give an error (missing codec)

## what is what

 - `tail_size`: each can hold a fixed number of bits, so the last frame has to be filled up with filler bits. `tail_size` is the number of these.
 - `repetitions`: how many consecutive frames should have the same 'binary mask' (a segment of the original binary sequence transformed into a mask for the frame). This redundancy helps mitigate data loss resulting from youtube's compression.
 - `patch_height`, `patch_width`: dimensions of a chunk of a frame that holds a single bit
 - `temp_path`: temporary directory for video creation. Will be deleted, so don't provide something with valuable data in it