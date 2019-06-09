#!/bin/bash

#Temp files
tmpdir="/tmp/ocrit/$USER"
imgfile="$tmpdir/image.jpg"
txtfile="$tmpdir/text"

#Dialog labels 
lang_title="ocr - language"
lang_text="Select source text language"
result_title="ocr - result text"

#List of languages for ocr
langs="rus eng"

#Delay
if [ $# -ne 0 ]; then
  sleep $1
fi


if [ ! -f $tmpdir ]; then
  mkdir $tmpdir -p
fi

gnome-screenshot -a --file "$imgfile" 
if [ ! -f $imgfile ]; then 
  exit
fi

ocrlang=$(zenity --list --column="language" --hide-header --text "$lang_text" --title "$lang_title" $langs | cut -f 1 -d '|')
if [ -n "$ocrlang" ]; then
  tesseract "$imgfile" "$txtfile" -l $ocrlang
  zenity --text-info --title "$result_title" --filename="$txtfile.txt"
  rm $txtfile.txt
fi

rm $imgfile
