default: install

.PHONY: check diff install default sudo-install 

install:
	# Install cmds at ~/.local/bin folder
	@ cp -r bin/*[^~] $(HOME)/.local/bin/
	# Done.


sudo-install:
	# Install cmds at /bin folder
	@ sudo cp bin/*[^~] /bin/
	# Done.

check:
	# Compare if cmds were changed
	# If so run `make' to update them
	@set -eu; \
	for src in bin/*; do \
		[ -f "$$src" ] || continue; \
		name=$${src##*/}; \
		dst="$$HOME/.local/bin//$$name"; \
		if [ ! -f "$$dst" ] || ! cmp -s "$$src" "$$dst"; then \
			printf '%s\n' "$$name"; \
		fi; \
	done

diff:
	# Diff if cmds were changed
	# If so run `make' to update them
	@diff -qr bin "$$HOME/.local/bin" || true


# Note make diff and check are similar
# But `make diff' also shows which files are missing and where