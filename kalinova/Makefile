# Makefile for Kalinova

.PHONY: install dev test lint clean run build-deb

# Install production dependencies
install:
	pip install -r requirements.txt

# Install for development (editable mode)
dev:
	pip install -e ".[dev]"

# Run the application
run:
	python -m kalinova.main

# Run all tests
test:
	pytest tests/ -v --cov=src/kalinova --cov-report=term-missing

# Run only unit tests
test-unit:
	pytest tests/unit/ -v

# Run only integration tests
test-integration:
	pytest tests/integration/ -v

# Lint code
lint:
	flake8 src/ --max-line-length=100
	mypy src/kalinova/

# Format code
format:
	black src/ tests/

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build .deb package
build-deb:
	@echo "Building .deb package..."
	mkdir -p build/deb/opt/kalinova
	mkdir -p build/deb/usr/share/applications
	mkdir -p build/deb/DEBIAN
	cp -r src/kalinova build/deb/opt/kalinova/
	cp packaging/control build/deb/DEBIAN/control
	cp packaging/postinst build/deb/DEBIAN/postinst
	cp packaging/prerm build/deb/DEBIAN/prerm
	chmod 755 build/deb/DEBIAN/postinst build/deb/DEBIAN/prerm
	cp packaging/kalinova.desktop build/deb/usr/share/applications/
	dpkg-deb --build build/deb build/kalinova_1.0.0_amd64.deb
	@echo "Package built: build/kalinova_1.0.0_amd64.deb"
