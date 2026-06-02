-- Save Pasted Image
-- Grabs the PNG image currently on the clipboard, asks the user which
-- folder to save it in, and writes it there with a timestamped filename.

on run
	-- 1. Make sure there is actually an image on the clipboard before we
	--    bother the user with a folder picker.
	set pngImage to missing value
	try
		set pngImage to (the clipboard as «class PNGf»)
	on error
		try
			-- Some apps put a TIFF on the clipboard instead of a PNG.
			-- Coerce it so we still get something to save.
			set pngImage to (the clipboard as «class TIFF»)
		on error
			display notification "No image found on the clipboard." with title "Save Pasted Image"
			return
		end try
	end try

	-- 2. Ask where to save it. A cancelled dialog just quietly exits.
	set targetFolder to missing value
	try
		set targetFolder to (choose folder with prompt "Save the pasted image in:")
	on error number -128
		-- User pressed Cancel.
		return
	end try

	-- 3. Build a unique, timestamped filename.
	set timeStamp to do shell script "date +%Y-%m-%d_%H-%M-%S"
	set fileName to "pasted-image-" & timeStamp & ".png"
	set folderPath to POSIX path of targetFolder
	if folderPath does not end with "/" then set folderPath to folderPath & "/"
	set destPath to folderPath & fileName

	-- 4. Write the bytes to disk.
	try
		set fileRef to (open for access (POSIX file destPath) with write permission)
		set eof of fileRef to 0
		write pngImage to fileRef
		close access fileRef
	on error errMsg
		try
			close access (POSIX file destPath)
		end try
		display notification errMsg with title "Save Pasted Image — failed"
		return
	end try

	-- 5. Put the saved file's full path on the clipboard. We use pbcopy
	--    rather than `set the clipboard to`, which doesn't reliably take
	--    effect from osascript launched in Alfred's background context.
	do shell script "printf %s " & quoted form of destPath & " | pbcopy"

	-- 6. Append a debug line so we can always see where files actually went.
	do shell script "printf '%s\\t%s\\n' \"$(date)\" " & quoted form of destPath & " >> \"$HOME/Library/Logs/save-pasted-image.log\""

	-- 7. Reveal the saved file in Finder so the destination is unambiguous,
	--    then notify.
	try
		tell application "Finder"
			reveal (POSIX file destPath as alias)
			activate
		end tell
	end try
	display notification destPath with title "Saved pasted image — path copied"
	return destPath
end run
