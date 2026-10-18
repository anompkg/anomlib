default: check

.PHONY: check diff install default sudo-install 

# Alias for install
it: install

install:
	# Installing commands at ~/.local/bin folder
	@ cp -r bin/*[^~] $(HOME)/.local/bin/
	# Done.


sudo-install:
	# Installing commands at /bin folder
	@ sudo cp bin/*[^~] /bin/
	# Done.

check:
	# Comparing if any commands changed
	# If so: run `make install' or just `make it' to update them
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
	# Diff which commands might change
	# If so: run `make install' or just `make it' to update them
	# Destination: $(HOME)/.local/bin
	@diff -qr bin "$$HOME/.local/bin" || true


# Note make diff and check are similar
# But `make diff' also shows which files are missing and where
