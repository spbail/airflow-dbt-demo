FROM quay.io/astronomer/ap-airflow:2.0.0-buster-onbuild

ENV AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor