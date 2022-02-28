from .qrmaster import  *
import  logging
import  uuid
from flask import Blueprint, send_file, request
from utils.format import err_msg, ok_msg_with

def views_api_qrencode(args):
    version, level, qr_name, output = qrencode(args.get('text'))
    logging.info(f'{version}{level}{qr_name}')
    filename = f'{uuid.uuid1()}.png'
    return send_file(output, as_attachment=True,
                     attachment_filename=filename,
                     mimetype='image/png')

def views_api_qrdecode():
    if 'file' not in request.files:
        return err_msg("400", "no qr image file")
    file = request.files['file']
    return ok_msg_with(qrdecode(file.read()))
