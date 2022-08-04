from flask import Flask, render_template, request, flash

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)
app.secret_key = "EL317PaL"

@app.route("/before")
def index():
    flash("---Input---")
    flash("---output---")
    return render_template("index.html")

@app.route("/go", methods=["POST", "GET"])
def go():
    Insen = request.form['sentence']
    Insub = request.form['subject']

    output = ["", "", ""] # store output sentence
    subject = [""] # subjevt of reply sentence (ex: So do ○.)
    sentence = Insen
    output[2] = subject[0] = subject_sep = Insub

# Word-separation
    sentence = nltk.word_tokenize(sentence) 
    subject_sep = nltk.word_tokenize(subject_sep)
            
# POS tagging
    pos = nltk.pos_tag(sentence)
    pos2 = nltk.pos_tag(subject_sep)
            
    for i in range(1, len(sentence)):
        if(pos[i][1] == 'MD'): # Find auxiliary verb
            if (pos[i][0] == 'wo'):
                output[1] = 'will'
            elif (pos[i][0] == 'ca'):
                output[1] = 'can'
            else:
                output[1] = pos[i][0]
            break
        elif ((pos[i][0] == 'have') or (pos[i][0] == "'ve") or (pos[i][0] == 'has') or (pos[i][0] == 'had')) and ((pos[i+1][1] == 'VBN') or (pos[i+1][1] == 'RB') or (pos[i+1][0] == 'already')):  # Find have(has) + Vpp
            output[1] = 'hav'
            break
        elif (pos[i][0] == 'had') and ((pos[i+1][1] == 'VBN') or (pos[i+1][1] == 'RB') or (pos[i+1][0] == 'already')):  # Find had + Vpp
            output[1] = 'had'
            break
        elif (pos[i][0] == 'am') or (pos[i][0] == "'m") or (pos[i][0] == 'is') or (pos[i][0] == "'s") or (pos[i][0] == 'are') or (pos[i][0] == "'re"):  # Find be verb(present).
            if (output[2] == 'I'):
                output[1] = 'am'
            elif (output[2] == 'you') or (output[2] == 'they') or (output[2] == 'we'):
                output[1] = 'are'
            else:
                output[1] = 'is'
            break
        elif (pos[i][0] == 'was') or (pos[i][0] == 'were'): # Find be verb(past).
            if (output[2] == 'you') or (output[2] == 'they') or (output[2] == 'we'):
                output[1] = 'were'
            else:
                output[1] = 'was'
            break
        elif(pos[i][1] == 'VBP') or (pos[i][1] == 'VBZ'): # Find Simple present
            output[1] = 'vb'
            break
        elif(pos[i][1] == 'VBD'):  # Find Simple past
            output[1] = 'vbd'
            break
            
# Decide So or Neither.
    for i in range(0, len(sentence)):                   
        if (pos[i][0] == 'not') or (pos[i][0] == "n't") or (pos[i][0] == 'never'):
            output[0] = 'Neither'
    if output[0] == "":
        output[0] = 'So'
            
# Find  and
    and_flag = 0
    for i in range(0, len(subject_sep)): 
        if subject_sep[i] == 'and':
            and_flag = 1
            
# Decide have or has according to subject
    if(output[1] == 'hav') and ((output[2] == "I") or (output[2] == "you") or (output[2] == "they") or (pos2[0][1] == "NNS") or (and_flag == 1)):
        output[1] = 'have'
    elif(output[1] == 'hav') and ((output[2] == "he") or (output[2] == "she") or (output[2] == "NNP") or (output[2] == "NN") or (len(subject_sep) != 1)):
        output[1] = 'has'
            
# Decide do or does or did according to subject
    elif(output[1] == 'vb') and ((output[2] == "I") or (output[2] == "you") or (output[2] == "they") or (pos2[0][1] == "NNS") or (and_flag == 1)):
        output[1] = 'do'
    elif(output[1] == 'vb') and ((output[2] == "he") or (output[2] == "she") or (pos2[0][1] == "NNP") or (pos2[0][1] == "NN") or (len(subject_sep) != 1)):
        output[1] = 'does'
    elif(output[1] == 'vbd'):
        output[1] = 'did'
              
# Output reply sentence
    if output[2] == "i":
        output[2] ="I"
    flash("Input Sentence : "+Insen)
    flash("Input Subject : "+Insub)
    flash(" ")
    flash("Output: "+ output[0]+" "+ output[1] +" "+ output[2]+".")
    return render_template("index.html")