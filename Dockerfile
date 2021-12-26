FROM public.ecr.aws/lambda/python:3.8

COPY ./docker/lambda/* ${LAMBDA_TASK_ROOT}
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["lambda_function.lambda_handler"]
