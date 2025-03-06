# Create __init__.py files for packages
# models/__init__.py
touch models/__init__.py
echo "# Models package" > models/__init__.py

# components/__init__.py
touch components/__init__.py
echo "# Components package" > components/__init__.py

# utils/__init__.py
touch utils/__init__.py
echo "# Utils package" > utils/__init__.py

# requirements.txt
cat << EOF > requirements.txt
streamlit
pandas
matplotlib
EOF
