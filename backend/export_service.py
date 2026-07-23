import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def build_csv(records):
    output = io.StringIO()
    writer = csv.writer(output)
    header = [
        "id",
        "location",
        "latitude",
        "longitude",
        "request_date",
        "start_date",
        "end_date",
        "temperature",
        "humidity",
        "wind_speed",
        "weather_condition",
        "forecast_data",
    ]
    writer.writerow(header)
    for record in records:
        writer.writerow([
            record.id,
            record.location,
            record.latitude,
            record.longitude,
            record.request_date.isoformat(),
            record.start_date.isoformat(),
            record.end_date.isoformat(),
            record.temperature,
            record.humidity,
            record.wind_speed,
            record.weather_condition,
            record.forecast_data,
        ])
    return output.getvalue().encode("utf-8")


def build_pdf(records):
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    title = Paragraph("Weather Requests Export", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    table_data = [
        [
            "ID",
            "Location",
            "Request",
            "Temp",
            "Humidity",
            "Wind",
            "Condition",
        ]
    ]
    for record in records:
        table_data.append([
            record.id,
            record.location,
            record.request_date.strftime("%Y-%m-%d"),
            f"{record.temperature}",
            f"{record.humidity}",
            f"{record.wind_speed}",
            record.weather_condition,
        ])
    table = Table(table_data, hAlign="LEFT")
    table.setStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]
    )
    elements.append(table)
    doc.build(elements)
    return output.getvalue()
