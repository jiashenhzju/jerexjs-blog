import { createReadStream, existsSync, statSync } from "node:fs";
import { basename, extname, resolve, sep } from "node:path";

const parseRange = (header, size) => {
  const match = /^bytes=(\d*)-(\d*)$/.exec(header ?? "");
  if (!match) return null;

  let start;
  let end;
  if (match[1] === "") {
    const suffix = Number(match[2]);
    if (!Number.isFinite(suffix) || suffix <= 0) return null;
    start = Math.max(0, size - suffix);
    end = size - 1;
  } else {
    start = Number(match[1]);
    end = match[2] === "" ? size - 1 : Number(match[2]);
  }

  if (
    !Number.isInteger(start) ||
    !Number.isInteger(end) ||
    start < 0 ||
    end < start ||
    start >= size
  ) {
    return null;
  }
  return { start, end: Math.min(end, size - 1) };
};

/**
 * Dev-only PDF library.
 *
 * PDFs live outside `public/`, so Astro never copies them into `dist/`.
 * The route supports byte ranges, allowing PDF.js to fetch large files in
 * chunks. `PAPER_LIBRARY_DIR` may point to an external disk; otherwise the
 * ignored `<repo>/local-papers/` directory is used.
 */
export function localPdfDevServer({ base = "/" } = {}) {
  const basePath = base === "/" ? "" : `/${base.replace(/^\/+|\/+$/g, "")}`;
  // Vite may pass either the original request URL or a base-stripped URL to
  // plugin middleware, depending on where the plugin sits in the stack.
  const prefixes = [
    `${basePath}/__local-pdf/`,
    "/__local-pdf/",
  ].filter((value, index, all) => all.indexOf(value) === index);

  return {
    name: "jerex-local-pdf-dev-server",
    apply: "serve",
    configureServer(server) {
      const libraryRoot = resolve(
        process.env.PAPER_LIBRARY_DIR || resolve(process.cwd(), "local-papers"),
      );

      server.middlewares.use((req, res, next) => {
        let pathname;
        try {
          pathname = new URL(req.url ?? "/", "http://localhost").pathname;
        } catch {
          return next();
        }
        const prefix = prefixes.find((candidate) => pathname.startsWith(candidate));
        if (!prefix) return next();

        let relativePath;
        try {
          relativePath = decodeURIComponent(pathname.slice(prefix.length));
        } catch {
          res.statusCode = 400;
          return res.end("Invalid PDF path");
        }

        const filePath = resolve(libraryRoot, relativePath);
        const insideLibrary =
          filePath.startsWith(`${libraryRoot}${sep}`) &&
          extname(filePath).toLowerCase() === ".pdf";
        if (!insideLibrary || !existsSync(filePath)) {
          res.statusCode = 404;
          return res.end("Local PDF not found");
        }

        const stat = statSync(filePath);
        if (!stat.isFile()) {
          res.statusCode = 404;
          return res.end("Local PDF not found");
        }

        res.setHeader("Content-Type", "application/pdf");
        res.setHeader("Accept-Ranges", "bytes");
        res.setHeader("Cache-Control", "private, no-store");
        res.setHeader(
          "Content-Disposition",
          `inline; filename="${basename(filePath).replaceAll('"', "")}"`,
        );

        const rangeHeader = req.headers.range;
        if (rangeHeader) {
          const range = parseRange(rangeHeader, stat.size);
          if (!range) {
            res.statusCode = 416;
            res.setHeader("Content-Range", `bytes */${stat.size}`);
            return res.end();
          }
          res.statusCode = 206;
          res.setHeader(
            "Content-Range",
            `bytes ${range.start}-${range.end}/${stat.size}`,
          );
          res.setHeader("Content-Length", range.end - range.start + 1);
          if (req.method === "HEAD") return res.end();
          return createReadStream(filePath, range).pipe(res);
        }

        res.statusCode = 200;
        res.setHeader("Content-Length", stat.size);
        if (req.method === "HEAD") return res.end();
        return createReadStream(filePath).pipe(res);
      });
    },
  };
}
