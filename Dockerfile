FROM python:3.14-slim

WORKDIR /app

# Install curl and Doppler
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -sLf --retry 3 --tlsv1.2 --proto "=https" \
    'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | \
    gpg --dearmor -o /usr/share/keyrings/doppler-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/doppler-archive-keyring.gpg] \
    https://packages.doppler.com/public/cli/deb/debian any-version main" | \
    tee /etc/apt/sources.list.d/doppler-cli.list && \
    apt-get update && apt-get install -y doppler && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv pip install --system -r pyproject.toml --no-dev-deps 2>/dev/null || \
    pip install fastapi uvicorn openai pymupdf pdfplumber python-dotenv python-multipart httpx

# Copy and install wheel
COPY dist/*.whl /tmp/
RUN pip install /tmp/*.whl --no-deps

EXPOSE 80

ENTRYPOINT ["doppler", "run", "--"]
CMD ["sh", "-c", "uvicorn resume_scanner.main:app --host ${HOST} --port ${PORT}"]
