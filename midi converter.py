import mido
from tkinter import Tk, filedialog, Label, Button, Text, END

def midi_to_text(midi_file, output_file):
    mid = mido.MidiFile(midi_file)
    events = []
    
    ticks_per_beat = mid.ticks_per_beat
    tempo = mido.bpm2tempo(120)  # default tempo is 120 bpm if a set tempo is not found
    
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                break
    
    for track in mid.tracks:
        note_on_times = {} 
        time = 0
        
        for msg in track:
            time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                # record start time
                note_on_times[msg.note] = mido.tick2second(time, ticks_per_beat, tempo)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in note_on_times:
                    start_time = note_on_times[msg.note]
                    end_time = mido.tick2second(time, ticks_per_beat, tempo)
                    key = str(msg.note)
                    # formating yay
                    events.append(f"{start_time:.3f},{end_time:.3f}'{key}'")
                    del note_on_times[msg.note]
    
    # save
    with open(output_file, 'w') as f:
        for event in events:
            f.write(event + '\n')

def open_file():
    midi_file = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid *.midi")])
    if midi_file:
        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_file:
            midi_to_text(midi_file, output_file)
            text_display.insert(END, f"Converted {midi_file} to {output_file}\n")

root = Tk()
root.title("MIDI to Text Converter")

label = Label(root, text="MIDI to Text Converter")
label.pack(pady=10)

convert_button = Button(root, text="Select MIDI File", command=open_file)
convert_button.pack(pady=10)

text_display = Text(root, height=10, width=50)
text_display.pack(pady=10)

root.mainloop()
