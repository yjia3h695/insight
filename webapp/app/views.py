#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import request, session, render_template, redirect, url_for, jsonify
from app import app
import httplib2
from apiclient import discovery
from oauth2client import client
from predict import predict_segment_info
from read_calendar import read_calendar
from segment_lists import segment_lists
from views_processing import process_event, process_interval


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/calendar.readonly',
        redirect_uri=url_for('oauth2callback', _external=True))
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('calendar'))


@app.route('/calendar')
def calendar():
    try:    # Check if user authorized access to the calendar.
        if 'credentials' not in session:
            return redirect(url_for('oauth2callback'))
        credentials = client.OAuth2Credentials.from_json(
            session['credentials'])
        if credentials.access_token_expired:
            return redirect(url_for('oauth2callback'))
        else:
            http_auth = credentials.authorize(httplib2.Http())
        # Establish connection with user's calendar
        calender_service = discovery.build('calendar', 'v3', http_auth)
        # Options to customize user's preference on day start,day end,
        # Calendar selection: All calendar or primary calendar only.
        try:
            start_hrs = int(request.args.get('s_hr'))
            start_mins = int(request.args.get('s_min'))
            end_hrs = int(request.args.get('e_hr'))
            end_mins = int(request.args.get('e_min'))
            prim = int(request.args.get('prim'))
            output, interval = read_calendar(calender_service,
                                             start_hrs, start_mins,
                                             end_hrs, end_mins, prim)
        except:
            try:
                output, interval = read_calendar(calender_service)
            # In case of user have no upcoming event tomorrow.
            except:
                return render_template('no_schedule.html')
        # Obtain the primary address input.
        if 'prefer_address' not in session:
            return render_template('input.html')
        else:
            prefer_address = session['prefer_address']
        # Read in the upcoming events.
        event_lists = process_event(output, prefer_address)
        # Calculate the time interval between every events.
        time_interval = process_interval(interval)
        segments, motto = predict_segment_info(prefer_address)
        segment_list = segment_lists(segments)
        return render_template('calendar.html',
                               output=event_lists, interval=time_interval,
                               motto=motto, locations=segment_list,
                               address=prefer_address)
    except:
        return redirect(url_for('index'))


@app.route('/test')
def test():
    return render_template('no_schedule.html')


@app.route('/input')
def input():
    address = request.args.get('set_address')
    session['prefer_address'] = address
    return redirect(url_for('calendar'))


@app.route('/suggest')
def suggest():
    prefer_address = request.args.get('address')
    session['prefer_address'] = prefer_address
    segments, motto = predict_segment_info(prefer_address)
    segment_list = segment_lists(segments)
    return render_template('suggest.html', motto=motto, locations=segment_list,
                           address=prefer_address)


@app.route('/show_forecast')
def show_forecast():
    data = dict(address=session['prefer_address'])
    return jsonify(data)


@app.route('/slides')
def slides():
    return render_template('slide.html')


@app.route('/logout')
def logout():
    session.pop('credentials', None)
    session.pop('prefer_address', None)
    session.pop('address', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
