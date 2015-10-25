package main

import (
	"fmt"
		"log"
			"os"
				"os/exec"
					"syscall"
						"time"
						)

						func main() {
							fmt.Print()
								iosizecmd := exec.Command("stap", "bitesize-nd.stp")
									iosizecmd.Stdout = os.Stdout
										iosizecmd.Stderr = os.Stderr

											err := iosizecmd.Start()
												log.Println("pid:", iosizecmd.Process.Pid)
													go func(p *os.Process) {
															_ = <-time.After(1 * time.Minute)
																	err := p.Signal(syscall.SIGTERM)
																			if err != nil {
																						panic(err)
																								}

																									}(iosizecmd.Process)
																										if err != nil {
																												panic(err)
																													}

																														err = iosizecmd.Wait()
																															if err != nil {
																																	panic(err)
																																		}
																																		}:
