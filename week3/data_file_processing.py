import csv

class FileProcessor:
    """Class to handle file processing for different formats."""
    
    def __init__(self, file_path):
        self.file_path = file_path
    
    def process_file(self):
        """Determines file type and calls appropriate processing method."""
        if self.file_path.endswith(".csv"):
            return self._process_csv()
        elif self.file_path.endswith(".txt"):
            return self._process_txt()
        else:
            return "Unsupported file format."

    def _process_csv(self):
        """Processes CSV files."""
        data = []
        try:
            with open(self.file_path, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            return "CSV file not found."
        return data
    
    def _process_txt(self):
        """Processes TXT files."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.readlines()
        except FileNotFoundError:
            return "TXT file not found."
        return [line.strip() for line in content]

def main():
    """Main function to execute file processing."""
    file_path = input("Enter the file path: ")
    processor = FileProcessor(file_path)
    result = processor.process_file()
    
    print("\nProcessed Data:")
    if isinstance(result, list):
        for line in result:
            print(line)
    else:
        print(result)

# Run the main function when script is executed
if __name__ == "__main__":
    main()