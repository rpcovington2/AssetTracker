import json
import locale
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from web.models import *
from web import db
from datetime import datetime, timedelta
import requests
# from Teller_config import TELLER_ACCESS_TOKEN, TELLER_BASE_URL
from decimal import Decimal
import os
import sqlite3

db_name = "/home/warehouse/NFC_Server/AssetTracker"
jobs = []
locale.setlocale(locale.LC_ALL, '')
views = Blueprint('views', __name__)


@views.route("/", methods=["GET", "POST"])
# @login_required
def home():
    uid = request.args.get("uid", "")  # get UID from query string if exists
    # return redirect(url_for("views.list_assets"))
    return render_template("Dashboard.html", uid=uid)


@views.route("/tag", methods=["GET", "POST"])
# @login_required
def tag():
    uid = request.args.get("uid", "")  # get UID from query string if exists
    # return redirect(url_for("views.list_assets"))
    return render_template("SubmitForm.html", uid=uid)


@login_required
@views.route("/Profile")
def profile():
    return render_template("Profile.html")

@login_required
@views.route("/Issue", methods=["GET", "POST"])
def reportIssue():

    print("Issue submitted")

    return render_template("Tracker.html",
                           user=current_user)


@views.route("/checktag", methods=["GET", "POST"])
def checktag():
    db_name = "/home/warehouse/NFC_Server/AssetTracker"

    uid = None

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        uid = data.get("uid")
    elif request.method == "GET":
        uid = request.args.get("uid")

    if not uid:
        return jsonify({"error": "UID missing"}), 400

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM assets WHERE asset_id=?", (uid,))
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({
            "status": row[4],
            "asset": row[0],
            "description": row[1],
            "type": row[2],
            "location": row[3],
            "notes": row[5]
        })
    else:
        # 🚀 redirect to your form page if tag not found
        return redirect(url_for("views.tag", uid=uid))


@views.route("/new_tag_form")
def new_tag_form():
    uid = request.args.get("uid", "")

    return render_template("Addform.html", uid=uid)


@views.route("/submit_tag", methods=["POST"])
def new_record():
    db_name = "X:\\Scripts\\NFCServer\\web\\warehouse.db"
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    # Basic validation
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and Email are required"}), 400

    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO assets (asset_id, name, type, location_id, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get("name"),
            data.get("notes"),
            data.get("category"),
            data.get("email"),
            "Shop Floor",
            "N/A"
            # data.get("notes"),
            # data.get("created_at") or datetime.utcnow().isoformat()
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Record saved successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500



@views.route("/api/assets", methods=["GET"])
def list_assets():
    db_name = "X:\\Scripts\\NFCServer\\web\\warehouse.db"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT asset_id, name, type, status, location_id, notes FROM assets ORDER BY status DESC")
    rows = cur.fetchall()
    conn.close()

    assets = [
        {
            "id": r[0],
            "name": r[1],
            "category": r[2],
            "serial": r[3],
            "location": r[4],
            "notes": r[5],
        }
        for r in rows
    ]
    return jsonify(assets)

