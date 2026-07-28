from pathlib import Path
import re


class FileReaderTool:
    def __init__(self, root_dir="workspace"):
        self.root_dir = Path(root_dir).resolve()
        self.root_dir.mkdir(parents=True, exist_ok=True)

        self.allowed_extensions = {".txt", ".md", ".log", ".py", ".json", ".csv"}

    def _normalize_relative_path(self, relative_path):
        path = str(relative_path).strip()

        if not path:
            return None

        path = path.replace("\\", "/")

        if path.startswith(self.root_dir.name + "/"):
            path = path[len(self.root_dir.name) + 1:]

        if path.startswith("./"):
            path = path[2:]

        return path

    def _resolve_safe_path(self, relative_path):
        normalized = self._normalize_relative_path(relative_path)

        if not normalized:
            return None, "File path was empty."

        requested_path = (self.root_dir / normalized).resolve()

        if self.root_dir not in requested_path.parents and requested_path != self.root_dir:
            return None, "Access denied. Files must stay inside the workspace folder."

        return requested_path, None

    def read_file(self, relative_path):
        try:
            requested_path, error = self._resolve_safe_path(relative_path)
            if error:
                return error

            if not requested_path.exists():
                return f"File not found: {requested_path.name}"

            if not requested_path.is_file():
                return f"Not a file: {requested_path.name}"

            if requested_path.suffix.lower() not in self.allowed_extensions:
                return (
                    f"Unsupported file type: {requested_path.suffix}. "
                    f"Allowed types: {', '.join(sorted(self.allowed_extensions))}"
                )

            content = requested_path.read_text(encoding="utf-8")

            max_chars = 12000
            if len(content) > max_chars:
                content = content[:max_chars] + "\n\n[File truncated]"

            return content

        except UnicodeDecodeError:
            return "Could not read file as UTF-8 text."
        except Exception as error:
            return f"File read error: {error}"


class FileListerTool:
    def __init__(self, root_dir="workspace"):
        self.root_dir = Path(root_dir).resolve()
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def _normalize_relative_path(self, relative_path):
        path = str(relative_path).strip()

        if not path or path == ".":
            return ""

        path = path.replace("\\", "/")

        if path.startswith(self.root_dir.name + "/"):
            path = path[len(self.root_dir.name) + 1:]

        if path.startswith("./"):
            path = path[2:]

        return path

    def list_files(self, relative_dir=""):
        try:
            normalized = self._normalize_relative_path(relative_dir)
            target_dir = (self.root_dir / normalized).resolve()

            if self.root_dir not in target_dir.parents and target_dir != self.root_dir:
                return "Access denied. Files must stay inside the workspace folder."

            if not target_dir.exists():
                return f"Directory not found: {normalized or '.'}"

            if not target_dir.is_dir():
                return f"Not a directory: {normalized or '.'}"

            entries = []
            for item in sorted(target_dir.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                entries.append(f"{item.name}/" if item.is_dir() else item.name)

            if not entries:
                return "Directory is empty."

            return "\n".join(entries)

        except Exception as error:
            return f"File listing error: {error}"


class FileSearchTool:
    def __init__(self, root_dir="workspace"):
        self.root_dir = Path(root_dir).resolve()
        self.root_dir.mkdir(parents=True, exist_ok=True)

        self.allowed_extensions = {".txt", ".md", ".log", ".py", ".json", ".csv"}

    def _normalize_relative_path(self, relative_path):
        path = str(relative_path).strip()

        if not path:
            return ""

        path = path.replace("\\", "/")

        if path.startswith(self.root_dir.name + "/"):
            path = path[len(self.root_dir.name) + 1:]

        if path.startswith("./"):
            path = path[2:]

        return path

    def search_file(self, query_spec):
        """
        Expected formats:
        - "todo.md::lecture"
        - "project_log.txt::memory"
        - "lecture"
        Default search location is the whole workspace if no file is given.
        """
        try:
            query_spec = str(query_spec).strip()
            if not query_spec:
                return "Search query was empty."

            if "::" in query_spec:
                path_part, query_part = query_spec.split("::", 1)
                relative_path = self._normalize_relative_path(path_part)
                needle = query_part.strip()
                files = [self.root_dir / relative_path]
            else:
                needle = query_spec
                files = list(self.root_dir.rglob("*"))

            if not needle:
                return "Search query was empty."

            needle_lower = needle.lower()
            matches = []

            for path in files:
                if not path.is_file():
                    continue

                if path.suffix.lower() not in self.allowed_extensions:
                    continue

                try:
                    text = path.read_text(encoding="utf-8").splitlines()
                except Exception:
                    continue

                for i, line in enumerate(text, start=1):
                    if needle_lower in line.lower():
                        matches.append(f"{path.relative_to(self.root_dir)}:{i}: {line.strip()}")

                        if len(matches) >= 20:
                            return "\n".join(matches) + "\n[Search truncated]"

            if not matches:
                return f"No matches found for: {needle}"

            return "\n".join(matches)

        except Exception as error:
            return f"File search error: {error}"